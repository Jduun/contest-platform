import AceEditor from 'react-ace'
import 'ace-builds/src-noconflict/mode-python'
import 'ace-builds/src-noconflict/theme-dracula'
import 'ace-builds/src-noconflict/theme-chrome'
import 'ace-builds/src-noconflict/theme-crimson_editor'
import 'ace-builds/src-noconflict/theme-solarized_light'
import { useTheme } from '@/components/ui/theme-provider'

interface CodeEditorProps {
  code: string
  setCode: (code: string) => void
}

export function CodeEditor({ code, setCode }: CodeEditorProps) {
  const { theme, setTheme: _ } = useTheme()

  function onChange(newValue: string) {
    setCode(newValue)
  }

  return (
    <AceEditor
      mode="python"
      theme={theme === 'light' ? 'chrome' : 'dracula'}
      name="chrome"
      fontSize={16}
      editorProps={{ $blockScrolling: true }}
      value={code}
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
