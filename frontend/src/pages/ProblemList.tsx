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

export function ProblemList() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const [_username, setUsername] = useAtom(usernameAtom)
  const [problems, setProblems] = useState<Problem[] | []>([])
  const pageNumber = parseInt(searchParams.get("page") || "1")
  const problemsCountOnPage = 10
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
        .catch((_err: AxiosError) => {
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
            limit: problemsCountOnPage,
          },
        })
        .then((response) => {
          console.log(response.data)
          setProblems(response.data)
        })
        .catch((err: AxiosError) => {
          console.log(err)
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
            contest_id={undefined}
            title={problem.title}
            difficulty={problem.difficulty}
            showScore={false}
          />
        ))}
      </div>
      <PaginationOverflow
        basePath='/'
        lastPage={30}
        visibleCount={5}
        currentPage={pageNumber}
      />
    </div>
  )
}
