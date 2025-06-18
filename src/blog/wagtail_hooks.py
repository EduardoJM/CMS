import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from draftjs_exporter.dom import DOM
from wagtail import hooks
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    BlockElementHandler,
    InlineStyleElementHandler,
)


@hooks.register('register_rich_text_features')
def register_code_block_feature(features):
    """
    Registering the `code-block` feature, which uses the `code-block` Draft.js block type,
    and is stored as HTML with `<pre><code>` tags.
    """
    feature_name = 'code-block'
    type_ = 'code-block'

    control = {
        'type': type_,
        'label': '{}',
        'description': 'Code',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.BlockFeature(control)
    )

    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {
            'pre': BlockElementHandler(type_),
            'code': InlineStyleElementHandler('CODE'),
        },
        'to_database_format': {
            'block_map': {'code-block': {'element': 'code', 'wrapper': 'pre'}}
        },
    })

    features.default_features.append(feature_name)


@hooks.register('register_rich_text_features')
def register_prism(features):
    feature_name = 'prism'
    features.default_features.append(feature_name)

    features.register_editor_plugin(
        'draftail',
        feature_name,
        draftail_features.PluginFeature(
            {
                'type': feature_name,
            },
            js=[
                'draftail/vendor/prism.min.js',
                'draftail/vendor/immutable.min.js',
                'draftail/draftail-prism.js',
            ],
        ),
    )

"""
def code_entity_decorator(props):
    return DOM.create_element('pre', {
        'data-language': props['language'],
    }, props['children'])

class CodeEntityElementHandler(AtomicBlockEntityElementHandler):
    def get_attribute_data(self, attrs):
        return { 'language': attrs['data-language'] }

@hooks.register('register_rich_text_features')
def register_code_block_feature(features):
    features.default_features.append('code-block')
    feature_name = 'code-block'
    type_ = 'CODE-BLOCK'

    control = {
        'type': type_,
        'label': '$',
        'description': 'Code Block',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.EntityFeature(
            control,
            js=['draftail/code-block.js'],
            css={'all': ['draftail/code-block.css']}
        )
    )

    features.register_converter_rule('contentstate', feature_name, {
        # Note here that the conversion is more complicated than for blocks and inline styles.
        'from_database_format': {'pre[data-language]': CodeEntityElementHandler()},
        'to_database_format': {'entity_decorators': {type_: code_entity_decorator}},
    })

"""