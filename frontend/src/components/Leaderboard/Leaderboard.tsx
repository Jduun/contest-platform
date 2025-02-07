import { useState, useEffect } from 'react'
import axios from 'axios'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'

interface Contest {
  id: string | undefined
  name: string | undefined
  start_time: string
  end_time: string
}

interface LeaderboardEntry {
  user_id: string
  solved_count: number
  total_penalty: number
  solved_problems: string[]
  penalty_times: number[]
}

interface User {
  id: string
  username: string
  role_id: string
  registered_at: string
}

export function Leaderboard(contest: Contest) {
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([])
  const [users, setUsers] = useState<Record<string, User>>({})
  const [currentUser, setCurrentUser] = useState<User | null>(null)
  const [loading, setLoading] = useState<boolean>(true)
  const [maxTasks, setMaxTasks] = useState<number>(0)

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        setLoading(true)
        const token = localStorage.getItem('token')

        // Получаем данные текущего пользователя
        const currentUserResponse = await axios.get(
          `http://localhost/api/users/me`,
          {
            headers: { Authorization: `Bearer ${token}` },
          },
        )
        setCurrentUser(currentUserResponse.data)

        // Получаем лидерборд
        const leaderboardResponse = await axios.get(
          `http://localhost/api/contests/${contest.id}/leaderboard`,
          {
            headers: { Authorization: `Bearer ${token}` },
          },
        )

        const leaderboardData: LeaderboardEntry[] =
          leaderboardResponse.data.leaderboard
        setLeaderboard(leaderboardData)

        const maxTasksInData = leaderboardData.reduce(
          (max, entry) => Math.max(max, entry.solved_problems.length),
          0,
        )
        setMaxTasks(maxTasksInData)

        const userIds = leaderboardData.map((entry) => entry.user_id)
        const userPromises = userIds.map((id) =>
          axios.get(`http://localhost/api/users/${id}`, {
            headers: { Authorization: `Bearer ${token}` },
          }),
        )
        const userResponses = await Promise.all(userPromises)
        const usersData = userResponses.reduce(
          (acc, res) => ({
            ...acc,
            [res.data.id]: res.data,
          }),
          {} as Record<string, User>,
        )
        setUsers(usersData)
      } catch (error) {
      } finally {
        setLoading(false)
      }
    }

    if (contest.id) {
      fetchLeaderboard()
    }
  }, [contest.id])

  if (loading) {
    return <p>Loading leaderboard...</p>
  }

  return (
    <div>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Место</TableHead>
            <TableHead>Пользователь</TableHead>
            {Array.from({ length: maxTasks }, (_, i) => (
              <TableHead key={i}>Задача {i + 1}</TableHead>
            ))}
            <TableHead className="text-right">Суммарный штраф</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {leaderboard.map((entry, index) => {
            const isCurrentUser = currentUser?.id === entry.user_id
            return (
              <TableRow
                key={entry.user_id}
                className={isCurrentUser ? 'bg-blue-100 font-bold' : ''}
              >
                <TableCell>{index + 1}</TableCell>
                <TableCell>
                  {users[entry.user_id]?.username || 'Loading...'}
                </TableCell>
                {Array.from({ length: maxTasks }, (_, i) => {
                  const penalty =
                    entry.penalty_times[i] !== undefined
                      ? entry.penalty_times[i]
                      : '-'
                  return <TableCell key={i}>{penalty}</TableCell>
                })}
                <TableCell className="text-right">
                  {entry.total_penalty}
                </TableCell>
              </TableRow>
            )
          })}
        </TableBody>
      </Table>
    </div>
  )
}
