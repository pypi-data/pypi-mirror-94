from pollination_dsl.alias import OutputAlias
from queenbee.io.common import IOAliasHandler


"""Daylight factor recipe output.

The results are separated by line and the numbers cannot be more than 100.
"""
parse_daylight_factor_results = [
    OutputAlias.any(
        name='daylight_factor',
        description='Daylight factor values.',
        platform=['grasshopper'],
        handler=[
            IOAliasHandler(
                language='python',
                module='pollination_handlers.outputs.read_file',
                function='read_DF_from_path'
            )
        ]
    )
]
