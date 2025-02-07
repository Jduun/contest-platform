import 'ace-builds/src-noconflict/mode-python'
import 'ace-builds/src-noconflict/theme-dracula'
import 'ace-builds/src-noconflict/theme-chrome'
import 'ace-builds/src-noconflict/theme-crimson_editor'
import 'ace-builds/src-noconflict/theme-solarized_light'
import { useTheme } from '@/components/ui/theme-provider'
import { ActivityCalendar } from 'react-activity-calendar'
import { cloneElement, useState } from 'react'
import { Tooltip as ReactTooltip } from 'react-tooltip'
import 'react-tooltip/dist/react-tooltip.css'
import { YearCombobox } from '@/components/Combobox/YearCombobox'

interface CalendarProps {
  activityData: any
}

const skeletonLabels = {
  months: [
    'Jan',
    'Feb',
    'Mar',
    'Apr',
    'May',
    'Jun',
    'Jul',
    'Aug',
    'Sep',
    'Oct',
    'Nov',
    'Dec',
  ],
  weekdays: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
  totalCount: ' ',
  legend: {
    less: 'Less',
    more: 'More',
  },
}

const currentYear: number = new Date().getFullYear()
const skeletonActivityData = [
  {
    date: `${currentYear}-01-01`,
    count: 0,
    level: 0,
  },
  {
    date: `${currentYear}-12-31`,
    count: 0,
    level: 0,
  },
]

export function ExtendedActivityCalendar({ activityData }: CalendarProps) {
  const { theme, setTheme: _ } = useTheme()
  const [year, setYear] = useState(currentYear)

  const labels = {
    months: [
      'Jan',
      'Feb',
      'Mar',
      'Apr',
      'May',
      'Jun',
      'Jul',
      'Aug',
      'Sep',
      'Oct',
      'Nov',
      'Dec',
    ],
    weekdays: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
    totalCount: '{{count}} activities in {{year}}',
    legend: {
      less: 'Less',
      more: 'More',
    },
  }

  const getYearActivityData = () => {
    const firstDay = { date: `${year}-01-01`, count: 0, level: 0 }
    const lastDay = { date: `${year}-12-31`, count: 0, level: 0 }

    if (`${year}` in activityData) {
      const firstDayExists = activityData[`$year`]?.some(
        (item: any) => item.date === `${year}-01-01`,
      )
      if (!firstDayExists) {
        activityData[`${year}`].unshift(firstDay)
      }
      const lastDayExists = activityData[`$year`]?.some(
        (item: any) => item.date === `${year}-12-31`,
      )
      if (!lastDayExists) {
        activityData[`${year}`].push(lastDay)
      }
      return activityData[`${year}`]
    }
    return [firstDay, lastDay]
  }

  const getMinYearInActivityData = () => {
    if (activityData === null) {
      return currentYear
    }
    const minYear = Math.min(...Object.keys(activityData).map(Number))
    return minYear
  }

  return (
    <div>
      <div>
        <div className="py-2">
          <YearCombobox
            startYear={getMinYearInActivityData()}
            year={year}
            setYear={setYear}
          />
        </div>
        <div>
          {activityData !== null ? (
            <ActivityCalendar
              data={getYearActivityData()}
              //showWeekdayLabels={true}
              colorScheme={theme}
              labels={labels}
              theme={{
                light: ['#f0ecf4', '#585cf4'],
                dark: ['#181820', '#585cf4'],
              }}
              renderBlock={(block, activity) =>
                cloneElement(block, {
                  'data-tooltip-id': 'react-tooltip',
                  'data-tooltip-html': `${activity.count} activities on ${activity.date}`,
                })
              }
            />
          ) : (
            <ActivityCalendar
              data={skeletonActivityData}
              //showWeekdayLabels={true}
              colorScheme={theme}
              labels={skeletonLabels}
              theme={{
                light: ['#f0ecf4', '#585cf4'],
                dark: ['#181820', '#585cf4'],
              }}
            />
          )}
          <ReactTooltip id="react-tooltip" />
        </div>
      </div>
    </div>
  )
}
