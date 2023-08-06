import pkgutil
from pathlib import Path
from typing import Any, Dict, List, Optional

import typer
import yaml
from alteia.core.errors import ResponseError
from PyInquirer import Separator, Token, prompt, style_from_dict
from tabulate import tabulate

from alteia_cli import utils
from alteia_cli.sdk import alteia_sdk

app = typer.Typer()

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})


class Preprocessing:
    def __init__(self, operation: str, *, parameters: Dict = None):
        self.operation = operation
        self.parameters = parameters or {}

    def to_dict(self):
        return self.__dict__


class Input:
    def __init__(self, name: str, *, display_name: str, description: str,
                 required: bool, source: Dict = None, scheme: Dict = None,
                 preprocessings: List[Preprocessing] = None):
        self.name = name
        self.display_name = display_name
        self.required = required
        self.description = description
        if source:
            if source.get('scheme'):
                utils.check_json_schema(source['scheme'])
        self.source = source
        if scheme:
            utils.check_json_schema(scheme)
        self.scheme = scheme
        self.preprocessings = preprocessings or []

    def to_dict(self):
        return self.__dict__

    def to_dict_without_preprocessings(self):
        """ Used to match the analytic creation API """
        d = self.__dict__.copy()
        d.pop('preprocessings', None)
        return d

    def get_serialized_preprocessings_with_input_name(self):
        """ Used to match the analytic creation API """
        preprocessings = []
        for p in self.preprocessings:
            preprocessing_dict = p.to_dict()
            preprocessing_dict['input'] = self.name
            preprocessings.append(preprocessing_dict)
        return preprocessings

    @classmethod
    def from_yaml(cls, yaml_desc: Dict):
        kind = str(yaml_desc.get('kind'))
        scheme: Dict[str, Any]
        source: Dict[str, Any]

        if kind == 'dataset':
            scheme = {
                'type': 'string',
                'pattern': '^[0-9a-f]{24}$'
            }
        elif kind == 'dataset-array':
            scheme = {
                'type': 'array',
                'items': {
                    'type': 'string',
                    'pattern': '^[0-9a-f]{24}$'
                }
            }
        else:
            raise KeyError('kind {!r} not supported'.format(kind))

        source = {
            'service': 'data-manager',
            'resource': 'dataset'
        }

        dataset_schema = yaml_desc.get('schema')
        if dataset_schema:
            source.update({
                'scheme': {
                    'type': 'object',
                    'properties': {},
                    'required': []
                }
            })

            if dataset_schema.get('mission'):
                source['fromMissions'] = dataset_schema.pop('mission')

            for prop_name, possible_values in dataset_schema.items():
                if prop_name == 'categories':
                    if not possible_values:
                        # Ignore categories if empty
                        continue

                    source['scheme']['properties'][prop_name] = {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'contains': {'enum': possible_values}
                    }
                elif prop_name == 'type':
                    source['scheme']['properties'][prop_name] = {
                        'const': possible_values
                    }
                elif prop_name == 'source':
                    source['scheme']['properties']['source'] = {
                        'type': 'object',
                        'properties': {
                            'name': {
                                'const': possible_values
                            }
                        }
                    }
                else:
                    raise KeyError('{!r} not supported'.format(prop_name))
                source['scheme']['required'].append(prop_name)

            preprocessings = None
            if yaml_desc.get('preprocessings'):
                input_preprocessings = yaml_desc.get('preprocessings', [])
                preprocessings = [Preprocessing(operation=p.get('operation'),
                                                parameters=p.get('parameters'))
                                  for p in input_preprocessings]

        return cls(
            name=str(yaml_desc.get('name')),
            display_name=str(yaml_desc.get('display-name')),
            required=bool(yaml_desc.get('required')),
            description=str(yaml_desc.get('description')),
            scheme=scheme,
            source=source,
            preprocessings=preprocessings
        )


class Deliverable(Input):
    pass


class Parameter:
    def __init__(self, name: str, *, display_name: str, description: str,
                 required: bool, scheme: Dict = None, default_value: Optional[Any]):
        self.name = name
        self.display_name = display_name
        self.required = required
        self.description = description
        if scheme:
            utils.check_json_schema(scheme)
        self.scheme = scheme
        self.default_value = default_value

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_yaml(cls, yaml_desc: Dict):
        scheme = yaml_desc.get('schema')
        if scheme:
            default_value = scheme.get('default')
        return cls(
            name=str(yaml_desc.get('name')),
            display_name=str(yaml_desc.get('display-name')),
            required=bool(yaml_desc.get('required')),
            description=str(yaml_desc.get('description')),
            scheme=scheme,
            default_value=default_value
        )


class Analytic:
    def __init__(self, name: str, *, display_name: str, description: str,
                 docker_image: str,
                 instance_type: Optional[str] = None,
                 volume_size: Optional[int] = None,
                 tags: Optional[List[str]] = None, groups: List[str] = None,
                 inputs: Optional[List[Input]] = None,
                 parameters: Optional[List[Parameter]] = None,
                 deliverables: Optional[List[Deliverable]] = None):
        self.name = name
        self.display_name = display_name
        self.description = description
        self.docker_image = docker_image
        self.instance_type = instance_type
        self.volume_size = volume_size
        self.tags = tags
        self.groups = groups
        self.inputs = inputs
        self.parameters = parameters
        self.deliverables = deliverables

    @classmethod
    def from_yaml(cls, yaml_desc: Dict):
        creation_params: Dict[str, Any]
        creation_params = {
            'name': str(yaml_desc.get('name')),
            'display_name': str(yaml_desc.get('display-name')),
            'description': str(yaml_desc.get('description')),
            'docker_image': str(yaml_desc.get('docker-image')),
            'volume_size': yaml_desc.get('volume-size'),
            'instance_type': yaml_desc.get('instance-type'),
            'tags': yaml_desc.get('tags'),
            'groups': yaml_desc.get('groups'),
        }
        yaml_inputs = yaml_desc.get('inputs')
        if isinstance(yaml_inputs, list):
            creation_params['inputs'] = [Input.from_yaml(i) for i in yaml_inputs]
        yaml_deliv = yaml_desc.get('deliverables')
        if isinstance(yaml_deliv, list):
            creation_params['deliverables'] = [
                Deliverable.from_yaml(i) for i in yaml_deliv]
        yaml_params = yaml_desc.get('parameters')
        if isinstance(yaml_params, list):
            creation_params['parameters'] = [
                Parameter.from_yaml(i) for i in yaml_params]
        return cls(**creation_params)


def _get_analytic_schema(schema_path: str) -> Dict:
    file_content = pkgutil.get_data(
        __name__,
        schema_path
    )
    if file_content:
        return yaml.load(file_content, Loader=yaml.Loader)
    else:
        raise FileNotFoundError


ANALYTIC_DESC_SCHEMA = _get_analytic_schema('share/analytic_schema.yaml')


@app.command(name='list')
def list_analytics(
    limit: int = typer.Option(default=100, help='Max number of analytics returned')
):
    """ List the analytics """
    sdk = alteia_sdk()
    with utils.spinner():
        found_analytics = sdk.analytics.search(
            filter={'is_backoffice': {'$ne': True}},
            return_total=True,
            limit=limit,
            sort={'display_name': 1}
        )
        results = found_analytics.results

    if len(results) > 0:
        table = {
            'Analytic display name': [
                typer.style(r.display_name, fg=typer.colors.GREEN, bold=True)
                for r in results
            ],
            'Name': [r.name for r in results],
            'Identifier': [r.id for r in results]
        }
        print(tabulate(
            table,
            headers='keys',
            tablefmt='pretty',
            colalign=('left', 'left')
        ))

        print()
        print('{}/{} analytics displayed'.format(
            len(results),
            found_analytics.total
        ))

    else:
        print('No analytic found.')


@app.command()
def create(
    description: Path = typer.Option(
        ...,   # '...' in typer.Option() makes the option required
        exists=True,
        readable=True,
        help='Path of the Analytic description (YAML file)'),
    company: str = typer.Option(default=None, help='Company identifier'),
):
    """ Create a new analytic """
    analytic_desc = parse_analytic_yaml(description)
    analytic = Analytic.from_yaml(analytic_desc)
    typer.secho('✓ Analytic description is valid', fg=typer.colors.GREEN)
    sdk = alteia_sdk()
    found_analytics = sdk.analytics.search(name=analytic.name)
    if found_analytics:
        typer.secho(
            '⚠ {} already exists on {}'.format(
                analytic.name, sdk._connection._base_url
            ),
            fg=typer.colors.YELLOW
        )
        replace_confirm_msg = typer.style(
            'Would you like to replace it?', fg=typer.colors.YELLOW)
        typer.confirm(replace_confirm_msg, abort=True)
        sdk.analytics.delete(analytic=found_analytics[0].id)
    else:
        typer.secho(
            '✓ No analytic with the name {!r} on {!r}'.format(
                analytic.name, sdk._connection._base_url
            ),
            fg=typer.colors.GREEN
        )

    analytic_creation_params = {
        'name': analytic.name,
        'display_name': analytic.display_name,
        'description': analytic.description,
        'docker_image': analytic.docker_image,
    }

    inputs = None
    deliverables = None
    parameters = None
    preprocessings: Optional[List[Preprocessing]] = None

    if analytic.inputs:
        inputs = []
        preprocessings = []
        for i in analytic.inputs:
            inputs.append(i.to_dict_without_preprocessings())
            if i.preprocessings:
                preprocessings.extend(i.get_serialized_preprocessings_with_input_name())

        if not preprocessings:
            preprocessings = None

    if analytic.parameters:
        parameters = [p.to_dict() for p in analytic.parameters]
    if analytic.deliverables:
        deliverables = [d.to_dict() for d in analytic.deliverables]

    for sdk_param, obj_val in (('instance_type', analytic.instance_type),
                               ('volume_size', analytic.volume_size),
                               ('inputs', inputs),
                               ('parameters', parameters),
                               ('deliverables', deliverables),
                               ('tags', analytic.tags),
                               ('groups', analytic.groups),
                               ('company', company),
                               ('preprocessings', preprocessings)):
        if obj_val is not None:
            analytic_creation_params[sdk_param] = obj_val

    created_analytic = sdk.analytics.create(**analytic_creation_params)
    typer.secho('✓ Analytic created successfully', fg=typer.colors.GREEN)
    return created_analytic


def parse_analytic_yaml(analytic_yaml_path: Path) -> Dict:
    with open(analytic_yaml_path) as f:
        analytic = yaml.load(f, Loader=yaml.Loader)
    errors = utils.validate_against_schema(
        analytic,
        json_schema=ANALYTIC_DESC_SCHEMA
    )
    if errors:
        typer.secho(
            '✖ Cannot create the analytic with the supplied YAML file. '
            'Found error(s):',
            fg=typer.colors.RED
        )
        print(errors)
        raise typer.Exit(2)
    else:
        return analytic


def find_analytic(sdk, analytic_name):
    with utils.spinner():
        found_analytics = sdk.analytics.search(
            name=analytic_name,
            return_total=True,
            limit=10,
        )
        results = found_analytics.results

    if found_analytics.total == 1:
        return results[0]

    typer.secho(
        '✖ Cannot find the analytic {!r}'.format(analytic_name),
        fg=typer.colors.RED
    )
    raise typer.Exit(2)


@app.command()
def unshare(
        analytic_name: str = typer.Argument(...),
        company: str = typer.Option(default=None, help='Company identifier')):
    """ Unshare an analytic """
    sdk = alteia_sdk()

    def company_selection(analytic_current_companies):
        def validate_answer(answer):
            if len(answer):
                return True
            return 'You must choose at least company.'

        user = sdk._providers['auth_api'].post(
            '/describe-user', {'with_company_names': True})
        companies = user['companies']
        questions = [
            {
                'type': 'checkbox',
                'message': 'Select companies to unshare analytics',
                'name': 'form',
                'choices': [
                    Separator('The analytic will be unshared with :')
                ],
                'validate': validate_answer
            }
        ]

        number_of_comp_shared = 0
        for comp in companies:
            choice = {'name': comp['name'], 'value': comp['id']}
            if comp['id'] not in analytic_current_companies:
                number_of_comp_shared += 1
                choice['checked'] = True
                choice['disabled'] = 'Analytics is not on this company'
            questions[0]['choices'].append(choice)

        if number_of_comp_shared == len(companies):
            typer.secho(
                '✖ Analytics isn\'t on any company',
                fg=typer.colors.YELLOW
            )
            raise typer.Exit(2)

        form_answers = prompt(questions, style=style)
        companies_ids = form_answers['form']

        return companies_ids

    analytic = find_analytic(sdk, analytic_name=analytic_name)
    if not analytic.external:
        typer.secho(
            '✖ Cannot unshare the non-external analytic {!r}'.format(analytic_name),
            fg=typer.colors.RED
        )
        raise typer.Exit(2)
    try:
        analytic_id = analytic.id
        if company:
            sdk.analytics.unshare_with_company(
                analytic=analytic_id,
                company=company)
        else:
            companies = company_selection(analytic.companies)
            if not companies:
                typer.secho(
                    '✖ You should at least unshare '
                    'the analytic {!r} with one company'.format(analytic_name),
                    fg=typer.colors.YELLOW
                )
                raise typer.Exit(1)

            for company in companies:
                sdk.analytics.unshare_with_company(
                    analytic=analytic_id,
                    company=company)

    except ResponseError as e:
        typer.secho(
            '✖ Cannot unshare the analytic {!r}'.format(analytic_name),
            fg=typer.colors.RED
        )
        typer.secho('details: {}'.format(str(e)), fg=typer.colors.RED)
        raise typer.Exit(2)

    typer.secho(
        '✓ Analytic {!r} unshared successfully'.format(analytic_name),
        fg=typer.colors.GREEN
    )


@app.command()
def share(
        analytic_name: str = typer.Argument(...),
        company: str = typer.Option(default=None, help='Company identifier')):
    """ Share an analytic """
    sdk = alteia_sdk()

    def company_selection(analytic_current_companies):
        def validate_answer(answer):
            if len(answer):
                return True
            return 'You must choose at least one company.'

        user = sdk._providers['auth_api'].post(
            '/describe-user', {'with_company_names': True})
        companies = user['companies']
        print([c['name'] for c in companies])
        questions = [
            {
                'type': 'checkbox',
                'message': 'Select companies to share the analytic with',
                'name': 'form',
                'choices': [
                    Separator('The analytic will be shared with :')
                ],
                'validate': validate_answer
            }
        ]

        number_of_comp_shared = 0
        for comp in companies:
            choice = {'name': comp['name'], 'value': comp['id']}
            if comp['id'] in analytic_current_companies:
                number_of_comp_shared += 1
                choice['checked'] = True
                choice['disabled'] = 'This analytic is already shared with this company'
            questions[0]['choices'].append(choice)

        if number_of_comp_shared == len(companies):
            typer.secho(
                '✖ This analytic is already shared with all the companies',
                fg=typer.colors.YELLOW
            )
            raise typer.Exit(2)

        form_answers = prompt(questions, style=style)
        companies_ids = form_answers['form']

        return companies_ids

    analytic = find_analytic(sdk, analytic_name=analytic_name)
    if not analytic.external:
        typer.secho(
            '✖ Cannot share the non-external analytic {!r}'.format(analytic_name),
            fg=typer.colors.RED
        )
        raise typer.Exit(2)
    try:
        analytic_id = analytic.id
        if company:
            sdk.analytics.share_with_company(
                analytic=analytic_id,
                company=company)
        else:
            companies = company_selection(analytic.companies)
            if not companies:
                typer.secho(
                    '✖ You should at least share '
                    'the analytic {!r} with one company'.format(analytic_name),
                    fg=typer.colors.YELLOW
                )
                raise typer.Exit(1)

            for company in companies:
                sdk.analytics.share_with_company(
                    analytic=analytic_id,
                    company=company)

    except ResponseError as e:
        typer.secho(
            '✖ Cannot share the analytic {!r}'.format(analytic_name),
            fg=typer.colors.RED
        )
        typer.secho('details: {}'.format(str(e)), fg=typer.colors.RED)
        raise typer.Exit(2)

    typer.secho(
        '✓ Analytic {!r} shared successfully'.format(analytic_name),
        fg=typer.colors.GREEN
    )


@app.command()
def delete(analytic_name: str = typer.Argument(...)):
    """ Delete an analytic """
    sdk = alteia_sdk()
    analytic = find_analytic(sdk, analytic_name=analytic_name)

    if not analytic.external:
        deletion_confirm_msg = typer.style(
            'Analytic {!r} is NOT an external analytic. '
            'Are you sure you want to delete it anyway?'.format(analytic_name),
            fg=typer.colors.YELLOW)
        typer.confirm(deletion_confirm_msg, abort=True)
    try:
        analytic_id = analytic.id
        sdk.analytics.delete(analytic=analytic_id)
    except ResponseError as e:
        typer.secho(
            '✖ Cannot delete the analytic {!r}'.format(analytic_name),
            fg=typer.colors.RED
        )
        typer.secho('details: {}'.format(str(e)), fg=typer.colors.RED)
        raise typer.Exit(2)

    typer.secho(
        '✓ Analytic {!r} deleted successfully'.format(analytic_name),
        fg=typer.colors.GREEN
    )


if __name__ == "__main__":
    app()
