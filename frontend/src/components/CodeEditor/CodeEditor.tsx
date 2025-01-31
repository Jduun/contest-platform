import AceEditor from 'react-ace'
import 'ace-builds/src-noconflict/mode-python'
import 'ace-builds/src-noconflict/theme-dracula'
import 'ace-builds/src-noconflict/theme-chrome';
import 'ace-builds/src-noconflict/theme-crimson_editor'
import 'ace-builds/src-noconflict/theme-solarized_light'


interface CodeEditorProps {
  setCode: (code: string) => void
}

export function CodeEditor(CEProps: CodeEditorProps) {
  function onChange(newValue: string) {
    CEProps.setCode(newValue)
  }

  return (
    <AceEditor
      mode="python"
      //theme="dracula"
      name="chrome"
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
  )
}
