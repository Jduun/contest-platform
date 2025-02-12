import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { useState, useEffect } from 'react'
import axios, { AxiosError } from 'axios'
import { toast } from 'sonner'
import { Contest } from '@/dto'

export function ContestCard(contest: Contest) {
  const [joinContestStatus, setJoinContestStatus] = useState<boolean>(false)
  const navigate = useNavigate()

  const joinContest = async () => {
    const token = localStorage.getItem('token')
    await axios
      .post(`http://localhost/api/contests/${contest.id}/join`, null, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((response) => {
        console.log('response data: ', response.data)
      })
      .catch((err: AxiosError) => {
        console.log(err.message)
      })
      .finally(() => {
        setJoinContestStatus(true)
        toast('Вы успешно зарегистрировались!')
      })
  }

  const unjoinContest = async () => {
    const token = localStorage.getItem('token')
    await axios
      .delete(`http://localhost/api/contests/${contest.id}/unjoin`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((response) => {
        console.log('response data: ', response.data)
      })
      .catch((err: AxiosError) => {
        console.log(err.message)
      })
      .finally(() => {
        setJoinContestStatus(false)
        toast('Вы успешно отказались от участия!')
      })
  }

  useEffect(() => {
    const getJoinContestStatus = async () => {
      const token = localStorage.getItem('token')
      await axios
        .get(`http://localhost/api/contests/${contest.id}/join-status`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((response) => {
          console.log(response.data)
          setJoinContestStatus(response.data['join status'])
        })
    }
    getJoinContestStatus()
  }, [])

  return (
    <div className="py-2 w-full">
      <Card className="bg-primary flex justify-between">
        <CardHeader className="p-3">
          <CardTitle
            className="hover:underline cursor-pointer"
            onClick={() => {
              navigate(`/contests/${contest.id}`)
            }}
          >
            {contest.name}
          </CardTitle>
          <CardDescription>
            {contest.start_time} - {contest.end_time}
          </CardDescription>
        </CardHeader>
        {joinContestStatus ? (
          <Button
            className="m-4 bg-secondary text-red-600"
            onClick={() => {
              unjoinContest()
            }}
          >
            Отменить запись
          </Button>
        ) : (
          <Button
            className="m-4 bg-secondary text-green-500"
            onClick={() => {
              joinContest()
            }}
          >
            Присоединиться
          </Button>
        )}
      </Card>
    </div>
  )
}
