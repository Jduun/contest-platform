import axios, { AxiosError } from 'axios'
import { Navbar } from '@/components/Navbar/Navbar'
import { useNavigate } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { useParams } from 'react-router'
import 'react-tooltip/dist/react-tooltip.css'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { ExtendedActivityCalendar } from '@/components/ExtendedActivityCalendar/ExtendedActivityCalendar'

export function UserProfile() {
  const navigate = useNavigate()
  const params = useParams()
  const username = params.username
  const [activityData, setActivityData] = useState<[] | null>(null)

  useEffect(() => {
    const getActivityData = async () => {
      const token = localStorage.getItem('token')
      await axios
        .get(`http://localhost/api/users/profile/${username}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((response) => {
          setActivityData(response.data.activity_calendar)
          console.log(response.data)
          console.log(response.data.activity_calendar)
        })
        .catch((_err: AxiosError) => {
          navigate('/login')
          return
        })
    }
    getActivityData()
  }, [])

  return (
    <div className="flex flex-col w-full max-w-[900px] mx-auto">
      <Navbar />
      <div className="flex">
        <Avatar className="h-40 w-auto">
          <AvatarImage src="https://github.com/shadcn.png" />
          <AvatarFallback>
            <div className="w-40 h-40 rounded-full"></div>
          </AvatarFallback>
        </Avatar>
        <div className="px-6">
          <p className="text-4xl font-bold">{username}</p>
          <p className="text-xl font-bold">Solved problems</p>
          <p className="text-green-500 text-lg">Easy: {10}</p>
          <p className="text-yellow-500 text-lg">Medium: {15}</p>
          <p className="text-red-500 text-lg">Hard: {20}</p>
        </div>
      </div>

      <div className="py-6">
        <ExtendedActivityCalendar activityData={activityData} />
      </div>
    </div>
  )
}
