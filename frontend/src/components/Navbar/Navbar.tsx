import axios, { AxiosError } from 'axios'
import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuList,
} from '@/components/ui/navigation-menu'
import { ModeToggle } from '@/components/ui/mode-toggle'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { useAtom } from 'jotai'
import { usernameAtom } from '@/store/atoms'

interface UserInfo {
  username: string
}

export function Navbar() {
  const [username, setUsername] = useAtom(usernameAtom)
  const [avatarUrl, setAvatarUrl] = useState<string | null>(null)
  const navigate = useNavigate()

  useEffect(() => {
    const token = localStorage.getItem('token')
    axios
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
      })
  }, [])

  useEffect(() => {
    if (!username) return

    const token = localStorage.getItem('token')
    axios
      .get(`http://localhost/api/users/${username}/profile`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((response) => {
        //setAvatarUrl(response.data.avatar_url)
        setAvatarUrl(`${response.data.avatar_url}?v=${new Date().getTime()}`)
      })
  }, [username])

  return (
    <div className="flex justify-between items-center my-2">
      {/* Left Side */}
      <NavigationMenu>
        <NavigationMenuList className="flex space-x-6">
          <NavigationMenuItem>
            <Link to="/">Problems</Link>
          </NavigationMenuItem>
          <NavigationMenuItem>
            <Link to="/contests">Contests</Link>
          </NavigationMenuItem>
        </NavigationMenuList>
      </NavigationMenu>

      {/* Right Side */}
      <NavigationMenu>
        <NavigationMenuList className="flex space-x-3">
          <NavigationMenuItem>
            <ModeToggle />
          </NavigationMenuItem>
          <NavigationMenuItem>
            <Link to={`/users/${username}`}>
              <Avatar>
                {avatarUrl ? (
                  <>
                    <AvatarImage src={avatarUrl} />
                    <AvatarFallback>
                      {username?.charAt(0) ?? '?'}
                    </AvatarFallback>
                  </>
                ) : (
                  <AvatarFallback>{username?.charAt(0) ?? '?'}</AvatarFallback>
                )}
              </Avatar>
            </Link>
          </NavigationMenuItem>
        </NavigationMenuList>
      </NavigationMenu>
    </div>
  )
}
