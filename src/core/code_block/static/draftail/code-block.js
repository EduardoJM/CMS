class CodeBlockSource extends window.React.Component {
  componentDidMount() {
    const { editorState, entityType, onComplete } = this.props;

    console.log(entityType);

    const content = editorState.getCurrentContent();
    const selection = editorState.getSelection();

    // Uses the Draft.js API to create a new entity with the right data.
    const contentWithEntity = content.createEntity(
      entityType.type,
      'IMMUTABLE',
      { language: 'python' },
    );
    const entityKey = contentWithEntity.getLastCreatedEntityKey();

    // We also add some text for the entity to be activated on.
    const text = `def function(self):`;

    const newContent = window.DraftJS.Modifier.replaceText(
      content,
      selection,
      text,
      null,
      entityKey,
    );
    const nextState = window.DraftJS.EditorState.push(
      editorState,
      newContent,
      'insert-characters',
    );

    onComplete(nextState);
  }

  render() {
    return null;
  }
}

const CodeBlock = (props) => {
  const { entityKey, contentState } = props;
  const data = contentState.getEntity(entityKey).getData();

  console.log(data);

  return window.React.createElement(
    'pre',
    { 'data-language': data.language },
    props.children,
  );
};

window.draftail.registerPlugin({
  type: 'CODE-BLOCK',
  source: CodeBlockSource,
  decorator: CodeBlock,
}, 'entityTypes');
