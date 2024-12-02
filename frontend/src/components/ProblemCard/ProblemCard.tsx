import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { useNavigate } from 'react-router-dom'
import { Badge } from '@/components/ui/badge'

interface Problem {
  id: string
  title: string
  difficulty: string
}

export function ProblemCard(problem: Problem) {
  const navigate = useNavigate()
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

  return (
    <div className="py-2 w-full">
      <Card
        className="bg-primary hover:bg-secondary  cursor-pointer"
        onClick={() => {
          navigate(`/problems/${problem.id}`)
        }}
      >
        <CardHeader className="p-3">
          <CardTitle>{problem.title}</CardTitle>
          <CardDescription>
            <Badge
              variant="outline"
              className={difficultyColors[problem.difficulty]}
            >
              {difficultyToRussian[problem.difficulty]}
            </Badge>
          </CardDescription>
        </CardHeader>
      </Card>
    </div>
  )
}
