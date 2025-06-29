var KEY_SEPARATOR = '-';

function occupySlice(targetArr, start, end, componentKey) {
  for (var ii = start; ii < end; ii++) {
    targetArr[ii] = componentKey;
  }
}

const PrismOptions = Immutable.Record({
  defaultSyntax: null,
  filter: function (block) {
    return block.getType() === 'custom-code';
  },
  getSyntax: function (block) {
    if (block.getData) {
      return block.getData().get('syntax');
    }
    return null;
  },
  render: function (props) {
    return window.React.createElement(
      "span",
      { className: 'prism-token token ' + props.type },
      props.children
    )
  },
  prism: Prism,
});

function PrismDecorator(options) {
  this.options = PrismOptions(options || {});
  this.highlighted = {};
}

PrismDecorator.prototype.getDecorations = function(block) {
  var tokens, token, tokenId, resultId, offset = 0, tokenCount = 0;
  var filter = this.options.get('filter');
  var getSyntax = this.options.get('getSyntax');
  var blockKey = block.getKey();
  var blockText = block.getText();
  var decorations = Array(blockText.length).fill(null);
  var Prism = this.options.get('prism');
  var highlighted = this.highlighted;

  highlighted[blockKey] = {};

  if (!filter(block)) {
      return Immutable.List(decorations);
  }

  var syntax = getSyntax(block) || this.options.get('defaultSyntax');

  // Allow for no syntax highlighting
  if (syntax == null) {
      return Immutable.List(decorations);
  }

  // Parse text using Prism
  var grammar = Prism.languages[syntax];
  tokens = Prism.tokenize(blockText, grammar);

  function processToken(decorations, token, offset) {
    if (typeof token === 'string') {
      return
    }
    const tokenLength = token.length || token.content.length;
    //First write this tokens full length
    tokenId = 'tok'+(tokenCount++);
    resultId = blockKey + '-' + tokenId;
    highlighted[blockKey][tokenId] = token;
    occupySlice(decorations, offset, offset + tokenLength, resultId);
    //Then recurse through the child tokens, overwriting the parent
    var childOffset = offset;
    for (var i =0; i < token.content.length; i++) {
      var childToken = token.content[i];
      processToken(decorations, childToken, childOffset);
      childOffset += childToken.length;
    }
  }

  for (var i =0; i < tokens.length; i++) {
      token = tokens[i];
      processToken(decorations, token, offset);
      const tokenLength = token.length || token.content.length;
      offset += tokenLength;
  }

  return Immutable.List(decorations);
};

PrismDecorator.prototype.getComponentForKey = function(key) {
  return this.options.get('render');
};

PrismDecorator.prototype.getPropsForKey = function(key) {
  var parts = key.split('-');
  var blockKey = parts[0];
  var tokId = parts[1];
  var token = this.highlighted[blockKey][tokId];

  return {
      type: token.type
  };
};

const prismPlugin = {
  type: 'prism',
  decorators: [
    new PrismDecorator({
      getSyntax(block) {
        const data = block.getData();
        let language = data.get('language') || data.get('syntax');
        if (!language) {
          language = 'javascript';
        }
        if (typeof Prism.languages[language] === 'object') {
          return language;
        }
        return null;
      },
    }),
  ]
};

window.draftail.registerPlugin(prismPlugin, 'plugins');
