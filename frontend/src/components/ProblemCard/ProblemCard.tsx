import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Badge } from '@/components/ui/badge'
import axios, { AxiosError } from 'axios'
import { CheckIcon, Cross2Icon } from '@radix-ui/react-icons'

interface ProblemCardProps {
  id: string
  title: string
  difficulty: string
  showScore: boolean
  contest_id: string | undefined
}

export function ProblemCard(problemCardProps: ProblemCardProps) {
  const navigate = useNavigate()
  const [isSolved, setIsSolved] = useState<boolean | null>(null)

  const difficultyToRussian: Record<string, string> = {
    easy: 'Легкая',
    medium: 'Средняя',
    hard: 'Сложная',
  }
  const difficultyColors: Record<string, string> = {
    easy: 'text-green-500',
    medium: 'text-yellow-500',
    hard: 'text-red-500',
  }

  useEffect(() => {
    const token = localStorage.getItem('token')

    const getProblemIsSolved = async () => {
      await axios
        .get<boolean>(
          `http://localhost/api/problems/${problemCardProps.id}/is-solved`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        )
        .then((response) => {
          setIsSolved(response.data)
        })
    }
    getProblemIsSolved()
  }, [])

  return (
    <div className="py-2 w-full">
      <Card
        className="bg-primary hover:bg-secondary cursor-pointer flex justify-between"
        onClick={() => {
          if (problemCardProps.contest_id === undefined) {
            navigate(`/problems/${problemCardProps.id}`)
          } else {
            navigate(
              `/contests/${problemCardProps.contest_id}/problems/${problemCardProps.id}`,
            )
          }
        }}
      >
        <CardHeader className="p-3">
          <CardTitle>{problemCardProps.title}</CardTitle>
          <CardDescription>
            <Badge
              variant="outline"
              className={difficultyColors[problemCardProps.difficulty]}
            >
              {difficultyToRussian[problemCardProps.difficulty]}
            </Badge>
          </CardDescription>
        </CardHeader>
        <div className="m-6">
          {isSolved !== null ? (
            <div className="w-5 h-5">
              {isSolved ? (
                <CheckIcon className="w-full h-full text-green-500" />
              ) : (
                <Cross2Icon className="w-full h-full text-red-500" />
              )}
            </div>
          ) : (
            <></>
          )}
        </div>
      </Card>
    </div>
  )
}
