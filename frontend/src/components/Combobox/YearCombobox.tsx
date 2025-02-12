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
import { YearComboboxProps } from '@/dto'

const currentYear: number = new Date().getFullYear()

export function YearCombobox({ startYear, year, setYear }: YearComboboxProps) {
  const [open, setOpen] = React.useState(false)
  const yearRange = Array.from(
    { length: currentYear - startYear + 1 },
    (_, i) => startYear + i,
  )

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className="w-[100px] justify-between"
        >
          {year}
          <ChevronsUpDown className="opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[100px] p-0">
        <Command>
          <CommandList>
            <CommandEmpty>No language found.</CommandEmpty>
            <CommandGroup>
              {yearRange.map((yearToChoose) => (
                <CommandItem
                  key={yearToChoose}
                  value={`${yearToChoose}`}
                  onSelect={(currentValue) => {
                    setYear(Number(currentValue))
                    setOpen(false)
                  }}
                >
                  {yearToChoose}
                  <Check
                    className={cn(
                      'ml-auto',
                      year === yearToChoose ? 'opacity-100' : 'opacity-0',
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
