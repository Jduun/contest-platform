import AceEditor from 'react-ace';
import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/theme-dracula';

interface CodeEditorProps {
  setCode: (code: string) => void;
}

export function CodeEditor(CEProps: CodeEditorProps) {
  function onChange(newValue: string) {
    CEProps.setCode(newValue)
  }

  return (
    <AceEditor
      mode="python"
      theme="dracula"
      name="code_editor"
      fontSize={16}
      editorProps={{ $blockScrolling: true }}
      //value={CEProps.code}
      setOptions={{
        wrap: true,
        showLineNumbers: true,
        tabSize: 4,
      }}
      onChange={onChange}
      style={{ width: '100%', height: '510px' }}
    />
  );
};
