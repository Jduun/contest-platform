import axios, { AxiosError } from 'axios'
import { Navbar } from '@/components/Navbar/Navbar'
import { useNavigate } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { useParams } from 'react-router'
import 'react-tooltip/dist/react-tooltip.css'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { ExtendedActivityCalendar } from '@/components/ExtendedActivityCalendar/ExtendedActivityCalendar'
import { useAtom } from 'jotai'
import { usernameAtom } from '@/store/atoms'
import { UploadAvatar } from '@/components/UploadAvatar/UploadAvatar'
import { ProblemPieChart } from '@/components/PieChart/ProblemPieChart'
import { SolvedProblemsStats } from '@/dto'
import { Skeleton } from '@/components/ui/skeleton'

export function UserProfile() {
  const navigate = useNavigate()
  const params = useParams()
  const username = params.username
  const [activityData, setActivityData] = useState<[] | null>(null)
  const [avatarUrl, setAvatarUrl] = useState<string | null>(null)
  const [_username, _setUsername] = useAtom(usernameAtom)
  const [stats, setStats] = useState<SolvedProblemsStats>({
    easy: 0,
    medium: 0,
    hard: 0,
  })

  useEffect(() => {
    const token = localStorage.getItem('token')
    const setProfileData = async () => {
      await axios
        .get(`http://localhost/api/users/${username}/profile`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((response) => {
          setActivityData(response.data.activity_calendar)
          setAvatarUrl(`${response.data.avatar_url}?v=${new Date().getTime()}`) // to prevent browser caching
        })
        .catch((_err: AxiosError) => {
          navigate('/login')
        })
    }
    const setProblemStats = async () => {
      await axios
        .get(`http://localhost/api/stats/problems`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((response) => {
          setStats(response.data)
        })
        .catch((_err: AxiosError) => {
          navigate('/login')
        })
    }
    setProfileData()
    setProblemStats()
  }, [])

  return (
    <div className="flex flex-col w-full max-w-[900px] mx-auto">
      <Navbar />
      <div className="flex">
        <div className="flex flex-col">
          <Avatar className="h-52 w-52">
            {avatarUrl !== null ? (
              <>
                <AvatarImage src={avatarUrl} />
                <AvatarFallback>
                  <Skeleton className="h-52 w-52 rounded-full bg-primary" />
                </AvatarFallback>
              </>
            ) : (
              <AvatarFallback>
                <Skeleton className="h-52 w-52 rounded-full bg-primary" />
              </AvatarFallback>
            )}
          </Avatar>
          <UploadAvatar />
        </div>
        <div className="px-6">
          <p className="text-4xl font-bold">{username}</p>
          <p className="text-xl font-bold">Solved problems</p>
          <div>
            <ProblemPieChart {...stats} />
          </div>
        </div>
      </div>
      <div className="py-2">
        <ExtendedActivityCalendar activityData={activityData} />
      </div>
    </div>
  )
}
