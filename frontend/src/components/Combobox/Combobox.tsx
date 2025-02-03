import * as React from 'react'
import { Check, ChevronsUpDown } from 'lucide-react'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from '@/components/ui/command'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'
import { useAtom } from 'jotai'
import { programmingLanguageIdAtom } from '@/store/atoms'

const languages = [
  {
    value: '50',
    label: 'C (GCC 9.2.0)',
  },
  {
    value: '54',
    label: 'C++ (GCC 9.2.0)',
  },
  {
    value: '51',
    label: 'C# (Mono 6.6.0.161)',
  },
  {
    value: '60',
    label: 'Go (1.13.5)',
  },
  {
    value: '62',
    label: 'Java (OpenJDK 13.0.1)',
  },
  {
    value: '63',
    label: 'JavaScript (Node.js 12.14.0)',
  },
  {
    value: '67',
    label: 'Pascal (FPC 3.0.4)',
  },
  {
    value: '68',
    label: 'PHP (7.4.1)',
  },
  {
    value: '71',
    label: 'Python (3.8.1)',
  },
  {
    value: '72',
    label: 'Ruby (2.7.0)',
  },
  {
    value: '73',
    label: 'Rust (1.40.0)',
  },
  {
    value: '74',
    label: 'TypeScript (3.7.4)',
  },
]

export function Combobox() {
  const [open, setOpen] = React.useState(false)
  const [programmingLanguageId, setProgrammingLanguageId] = useAtom(programmingLanguageIdAtom)
  
  React.useEffect(() => {
      setProgrammingLanguageId(localStorage.getItem('programmingLanguageId') || '71')
    }, []
  )

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className="w-[200px] justify-between"
        >
          {programmingLanguageId
            ? languages.find((language) => language.value === programmingLanguageId)?.label
            : 'Выберите язык...'}
          <ChevronsUpDown className="opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[200px] p-0">
        <Command>
          <CommandInput placeholder="Поиск языка..." className="h-9" />
          <CommandList>
            <CommandEmpty>No language found.</CommandEmpty>
            <CommandGroup>
              {languages.map((language) => (
                <CommandItem
                  key={language.value}
                  value={language.value}
                  onSelect={(currentValue) => {
                    setProgrammingLanguageId(currentValue === programmingLanguageId ? '' : currentValue)
                    localStorage.setItem('programmingLanguageId', currentValue === programmingLanguageId ? '' : currentValue)
                    setOpen(false)
                  }}
                >
                  {language.label}
                  <Check
                    className={cn(
                      'ml-auto',
                      programmingLanguageId === language.value ? 'opacity-100' : 'opacity-0',
                    )}
                  />
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  )
}
