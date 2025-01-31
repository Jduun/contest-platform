import { useEffect, useState } from 'react'
import moment from 'moment'

interface CountdownTimerProps {
  endTime: string // time in ISO format
}

export function Timer({ endTime }: CountdownTimerProps) {
  const [timeLeft, setTimeLeft] = useState(() => calculateTimeLeft())

  function calculateTimeLeft() {
    const now = moment.utc()
    const end = moment.utc(endTime)
    const duration = moment.duration(end.diff(now))

    if (duration.asMilliseconds() <= 0) {
      return { days: 0, hours: 0, minutes: 0, seconds: 0 }
    }

    return {
      days: Math.floor(duration.asDays()),
      hours: duration.hours(),
      minutes: duration.minutes(),
      seconds: duration.seconds(),
    }
  }

  useEffect(() => {
    const timerId = setInterval(() => {
      setTimeLeft(calculateTimeLeft())
    }, 1000)

    return () => clearInterval(timerId)
  }, [endTime])

  return (
    <>
      {!isNaN(timeLeft.days) ? (
        <>
          {timeLeft.days === 0 &&
          timeLeft.hours === 0 &&
          timeLeft.minutes === 0 &&
          timeLeft.seconds === 0 ? (
            <p className="m-0 text-xs text-red-500">Контест закончился</p>
          ) : (
            <p className="m-0 text-xs">
              <span>До конца контеста осталось: </span>
              <span className="text-red-500">
                {timeLeft.days} дн. {timeLeft.hours} ч. {timeLeft.minutes} мин.{' '}
                {timeLeft.seconds} сек.
              </span>
            </p>
          )}
        </>
      ) : (
        <p className="m-0 text-xs">До конца контеста осталось:</p>
      )}
    </>
  )
}
