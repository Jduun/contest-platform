import AceEditor from 'react-ace'

import 'ace-builds/src-noconflict/mode-c_cpp'
import 'ace-builds/src-noconflict/mode-csharp'
import 'ace-builds/src-noconflict/mode-golang'
import 'ace-builds/src-noconflict/mode-java'
import 'ace-builds/src-noconflict/mode-pascal'
import 'ace-builds/src-noconflict/mode-php'
import 'ace-builds/src-noconflict/mode-python'
import 'ace-builds/src-noconflict/mode-rust'
import 'ace-builds/src-noconflict/mode-typescript'

import 'ace-builds/src-noconflict/theme-dracula'
import 'ace-builds/src-noconflict/theme-chrome'

import { useTheme } from '@/components/ui/theme-provider'
import { useAtom } from 'jotai'
import { programmingLanguageIdAtom } from '@/store/atoms'
import { programmingLanguagesAtom } from '@/store/atoms'
import { CodeEditorProps } from '@/dto'

export function CodeEditor({ code, setCode }: CodeEditorProps) {
  const { theme, setTheme: _ } = useTheme()
  const [programmingLanguageId, _setProgrammingLanguageId] = useAtom(
    programmingLanguageIdAtom,
  )
  const [programmingLanguages, _setProgrammingLanguages] = useAtom(
    programmingLanguagesAtom,
  )

  function onChange(newValue: string) {
    setCode(newValue)
  }

  return (
    <AceEditor
      mode={
        programmingLanguages.find(
          (language) => language.value === programmingLanguageId,
        )?.mode || programmingLanguages[0].mode
      }
      theme={theme === 'light' ? 'chrome' : 'dracula'}
      name="AceEditor"
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
