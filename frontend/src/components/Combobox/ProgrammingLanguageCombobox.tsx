import * as React from 'react'
import { Check, ChevronsUpDown } from 'lucide-react'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import {
  Command,
  CommandEmpty,
  CommandGroup,
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
import { programmingLanguagesAtom } from '@/store/atoms'

export function ProgrammingLanguageCombobox() {
  const [open, setOpen] = React.useState(false)
  const [programmingLanguageId, setProgrammingLanguageId] = useAtom(
    programmingLanguageIdAtom,
  )
  const [programmingLanguages, _setProgrammingLanguages] = useAtom(
    programmingLanguagesAtom,
  )

  React.useEffect(() => {
    setProgrammingLanguageId(
      localStorage.getItem('programmingLanguageId') ||
        programmingLanguages[0].value,
    )
  }, [])

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
            ? programmingLanguages.find(
                (language) => language.value === programmingLanguageId,
              )?.label
            : 'Выберите язык...'}
          <ChevronsUpDown className="opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[200px] p-0">
        <Command>
          <CommandList>
            <CommandEmpty>No language found.</CommandEmpty>
            <CommandGroup>
              {programmingLanguages.map((language) => (
                <CommandItem
                  key={language.value}
                  value={language.value}
                  onSelect={(currentValue) => {
                    setProgrammingLanguageId(
                      currentValue === programmingLanguageId
                        ? ''
                        : currentValue,
                    )
                    localStorage.setItem(
                      'programmingLanguageId',
                      currentValue === programmingLanguageId
                        ? ''
                        : currentValue,
                    )
                    setOpen(false)
                  }}
                >
                  {language.label}
                  <Check
                    className={cn(
                      'ml-auto',
                      programmingLanguageId === language.value
                        ? 'opacity-100'
                        : 'opacity-0',
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
