import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { CheckIcon, Cross2Icon } from '@radix-ui/react-icons'
import { ProblemCardProps } from '@/dto'
import { API_URL } from '@/api'

export function ProblemCard(problemCardProps: ProblemCardProps) {
  const navigate = useNavigate()
  const [isSolved, setIsSolved] = useState<boolean | null>(null)

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
          `${API_URL}/api/problems/${problemCardProps.id}/is-solved`,
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
    <div className="py-1 w-full">
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
          <CardDescription
            className={difficultyColors[problemCardProps.difficulty]}
          >
            {problemCardProps.difficulty}
          </CardDescription>
        </CardHeader>
        <div className="m-6">
          {isSolved !== null ? (
            <div className="w-4 h-4">
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
