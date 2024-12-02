import axios, { AxiosError } from 'axios'
import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Navbar } from '@/components/Navbar/Navbar'
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from '@/components/ui/pagination'
import { ProblemCard } from '@/components/ProblemCard/ProblemCard'
import { useAtom } from 'jotai'
import { usernameAtom } from '@/store/atoms'

interface UserInfo {
  username: string
}

interface Problem {
  id: string
  title: string
  statement: string
  memory_limit: number
  time_limit: number
  difficulty: string
}

export function ProblemList() {
  const navigate = useNavigate()
  const [username, setUsername] = useAtom(usernameAtom)
  const [problems, setProblems] = useState<Problem[] | []>([])

  useEffect(() => {
    const getUserInfo = async () => {
      const token = localStorage.getItem('token')
      await axios
        .get<UserInfo>('http://localhost/api/users/me', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((response) => {
          setUsername(response.data.username)
        })
        .catch((err: AxiosError) => {
          navigate('/login')
          return
        })
    }
    getUserInfo()

    const getProblems = async () => {
      const token = localStorage.getItem('token')
      await axios
        .get<Problem[]>('http://localhost/api/problems', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
          params: {
            offset: 0,
            limit: 10,
          },
        })
        .then((response) => {
          console.log(response.data)
          setProblems(response.data)
        })
    }
    getProblems()
  }, [])

  return (
    <div className="flex flex-col w-full max-w-[900px] mx-auto">
      <Navbar />
      <div>
        {problems.map((problem) => (
          <ProblemCard
            key={problem.id}
            id={problem.id}
            title={problem.title}
            difficulty={problem.difficulty}
          />
        ))}
      </div>
      <Pagination>
        <PaginationContent>
          <PaginationItem>
            <PaginationPrevious href="#" />
          </PaginationItem>
          <PaginationItem>
            <PaginationLink href="#">1</PaginationLink>
          </PaginationItem>
          <PaginationItem>
            <PaginationLink href="#">2</PaginationLink>
          </PaginationItem>
          <PaginationItem>
            <PaginationEllipsis />
          </PaginationItem>
          <PaginationItem>
            <PaginationNext href="#" />
          </PaginationItem>
        </PaginationContent>
      </Pagination>
    </div>
  )
}
