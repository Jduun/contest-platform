import axios, { AxiosError } from 'axios'
import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useSearchParams } from 'react-router-dom'
import { Navbar } from '@/components/Navbar/Navbar'
import { ProblemCard } from '@/components/ProblemCard/ProblemCard'
import { useAtom } from 'jotai'
import { usernameAtom } from '@/store/atoms'
import { Problem, UserInfo } from '@/dto'
import PaginationOverflow from '@/components/PagintationOverflow/PaginationOverflow'
import { Input } from '@/components/ui/input'
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { API_URL } from '@/api'

const difficultyColors: Record<string, string> = {
  easy: 'text-green-500',
  medium: 'text-yellow-500',
  hard: 'text-red-500',
}

export function ProblemList() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const [username, setUsername] = useAtom(usernameAtom)
  const [problems, setProblems] = useState<Problem[] | []>([])
  const [pagesCount, setPageCount] = useState<number>(1)
  const [searchInput, setSearchInput] = useState<string>('')
  const [difficulty, setDifficulty] = useState<string>('all')
  const [pageNumber, setPageNumber] = useState<number>(
    parseInt(searchParams.get('page') || '1'),
  )
  const problemsCountOnPage = 9

  interface ProblemsResponse {
    problems: Problem[]
    count: number
  }

  const fetchProblems = async () => {
    const token = localStorage.getItem('token')
    await axios
      .get<ProblemsResponse>(`${API_URL}/api/problems`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        params: {
          search_input: searchInput,
          difficulty: difficulty,
          offset: (pageNumber - 1) * problemsCountOnPage,
          limit: problemsCountOnPage,
        },
      })
      .then((response) => {
        setProblems(response.data.problems)
        setPageCount(Math.ceil(response.data.count / problemsCountOnPage))
      })
      .catch((err: AxiosError) => {
        console.log(err)
      })
  }

  useEffect(() => {
    const token = localStorage.getItem('token')
    const fetchUserInfo = async () => {
      await axios
        .get<UserInfo>(`${API_URL}/api/users/me`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((response) => {
          setUsername(response.data.username)
        })
        .catch((_err: AxiosError) => {
          navigate('/login')
          return
        })
    }
    if (!username) {
      fetchUserInfo()
    }
    //fetchProblems()
  }, [])

  useEffect(() => {
    fetchProblems()
  }, [searchInput, difficulty])

  return (
    <div className="flex flex-col w-full max-w-[900px] mx-auto">
      <Navbar />
      <div className="flex">
        <div className="pb-2 pr-2">
          <Input
            type="text"
            placeholder="Search problem"
            value={searchInput}
            onChange={(e) => {
              setPageNumber(1)
              setSearchInput(e.target.value)
            }}
          />
        </div>
        <div>
          <Select
            onValueChange={(value) => {
              setPageNumber(1)
              setDifficulty(value)
            }}
          >
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Select difficulty" />
            </SelectTrigger>
            <SelectContent>
              <SelectGroup>
                <SelectLabel>Difficulty</SelectLabel>
                <SelectItem value="all">
                  <p>all</p>
                </SelectItem>
                <SelectItem value="easy">
                  <p className={difficultyColors['easy']}>easy</p>
                </SelectItem>
                <SelectItem value="medium">
                  <p className={difficultyColors['medium']}>medium</p>
                </SelectItem>
                <SelectItem value="hard">
                  <p className={difficultyColors['hard']}>hard</p>
                </SelectItem>
              </SelectGroup>
            </SelectContent>
          </Select>
        </div>
      </div>
      <div>
        {problems.map((problem) => (
          <ProblemCard
            key={problem.id}
            id={problem.id}
            contest_id={undefined}
            title={problem.title}
            difficulty={problem.difficulty}
            showScore={false}
          />
        ))}
      </div>
      {pagesCount !== 1 ? (
        <PaginationOverflow
          basePath="/"
          lastPage={pagesCount}
          visibleCount={Math.min(5, pagesCount)}
          currentPage={pageNumber}
        />
      ) : (
        <></>
      )}
    </div>
  )
}
