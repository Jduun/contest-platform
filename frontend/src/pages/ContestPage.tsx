import { useParams } from 'react-router'
import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios, { AxiosError } from 'axios'
import { Navbar } from '@/components/Navbar/Navbar'
import { ProblemCard } from '@/components/ProblemCard/ProblemCard'
import moment from 'moment'
import { toast } from 'sonner'
import { Timer } from '@/components/Timer/Timer'
import { Leaderboard } from '@/components/Leaderboard/Leaderboard'

interface Contest {
  id: string
  name: string
  start_time: string
  end_time: string
}

interface Problem {
  id: string
  title: string
  statement: string
  memory_limit: number
  time_limit: number
  difficulty: string
}

export function ContestPage() {
  const navigate = useNavigate()
  const params = useParams()
  const id = params.id
  const [contest, setContest] = useState<Contest | null>(null)
  const [problems, setProblems] = useState<Problem[]>([])

  useEffect(() => {
    const getContest = async () => {
      const token = localStorage.getItem('token')
      await axios
        .get<Contest>(`http://localhost/api/contests/${id}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((response) => {
          setContest(response.data)
          console.log(response.status)
        })
        .catch((err: AxiosError) => {
          navigate('/contests')
        })
    }
    getContest()

    const getContestProblems = async () => {
      const token = localStorage.getItem('token')
      await axios
        .get<Problem[]>(`http://localhost/api/contests/${id}/problems`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((response) => {
          setProblems(response.data)
        })
        .catch((err: AxiosError) => {
          if (err.response?.status === 400) {
            toast('Контест еще не начался!')
          }
          navigate('/contests')
        })
    }
    getContestProblems()
  }, [])

  return (
    <div className="flex flex-col w-full max-w-[900px] mx-auto">
      <Navbar />
      <div className="prose dark:prose-invert">
        <div>
          <h1 className="m-0 text-3xl">{contest?.name}</h1>
          <p className="m-0 text-xs">
            Начало: {moment(contest?.start_time).format('LLL')}
            <br />
            Конец: {moment(contest?.end_time).format('LLL')}
            <br />
          </p>
          <Timer endTime={contest?.end_time || ''} />
        </div>
      </div>
      <div className="w-full">
        {problems.map((problem) => (
          <ProblemCard
            key={problem.id}
            id={problem.id}
            title={problem.title}
            difficulty={problem.difficulty}
            showScore={true}
            contest_id={id}
          />
        ))}
      </div>
      <Leaderboard
        key={contest?.id}
        id={contest?.id}
        name={contest?.name}
        start_time={moment(contest?.start_time).format('LLL')}
        end_time={moment(contest?.end_time).format('LLL')}
      />
    </div>
  )
}
