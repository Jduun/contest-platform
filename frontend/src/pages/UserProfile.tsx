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

export function UserProfile() {
  const navigate = useNavigate()
  const params = useParams()
  const username = params.username
  const [activityData, setActivityData] = useState<[] | null>(null)
  const [avatarUrl, setAvatarUrl] = useState<string | null>(null)
  const [_username, _setUsername] = useAtom(usernameAtom)

  useEffect(() => {
    const setProfileData = async () => {
      const token = localStorage.getItem('token')
      await axios
        .get(`http://localhost/api/users/${username}/profile`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((response) => {
          setActivityData(response.data.activity_calendar)
          //setAvatarUrl(response.data.avatar_url)
          setAvatarUrl(`${response.data.avatar_url}?v=${new Date().getTime()}`)
        })
        .catch((_err: AxiosError) => {
          navigate('/login')
        })
    }
    setProfileData()
  }, [])

  return (
    <div className="flex flex-col w-full max-w-[900px] mx-auto">
      <Navbar />
      <div className="flex">
        <div className="flex flex-col">
          <Avatar className="h-40 w-40">
            {avatarUrl !== null ? (
              <>
                <AvatarImage src={avatarUrl} />
                <AvatarFallback>
                  <div className="w-40 h-40 rounded-full"></div>
                </AvatarFallback>
              </>
            ) : (
              <AvatarFallback>
                <div className="w-40 h-40 rounded-full"></div>
              </AvatarFallback>
            )}
          </Avatar>
          <UploadAvatar />
        </div>
        <div className="px-6">
          <p className="text-4xl font-bold">{username}</p>
          <p className="text-xl font-bold">Solved problems</p>
          <p className="text-green-500 text-lg">Easy: {10}</p>
          <p className="text-yellow-500 text-lg">Medium: {15}</p>
          <p className="text-red-500 text-lg">Hard: {20}</p>
        </div>
      </div>
      <div className="py-2">
        <ExtendedActivityCalendar activityData={activityData} />
      </div>
    </div>
  )
}
