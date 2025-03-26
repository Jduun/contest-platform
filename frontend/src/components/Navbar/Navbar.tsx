import axios from 'axios'
import { useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuList,
} from '@/components/ui/navigation-menu'
import { ModeToggle } from '@/components/ui/mode-toggle'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { useAtom } from 'jotai'
import { usernameAtom , avatarUrlAtom, activityDataAtom } from '@/store/atoms'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { API_URL } from '@/api'

export function Navbar() {
  const [username, _setUsername] = useAtom(usernameAtom)
  const [avatarUrl, setAvatarUrl] = useAtom(avatarUrlAtom)
  const [activityData, setActivityData] = useAtom(activityDataAtom)
  const navigate = useNavigate()

  useEffect(() => {
    if (!username) return
    console.log(activityData)
    if (avatarUrl && activityData.length !== 0) return
    const token = localStorage.getItem('token')
    axios
      .get(`${API_URL}/api/users/${username}/profile`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((response) => {
        setActivityData(response.data.activity_calendar)
        setAvatarUrl(`${response.data.avatar_url}?v=${new Date().getTime()}`) // to prevent browser caching
      })
  }, [username])

  return (
    <div className="flex justify-between items-center my-2">
      {/* Left Side */}
      <NavigationMenu>
        <NavigationMenuList className="flex space-x-6">
          <NavigationMenuItem
            onClick={() => {
              window.location.reload()
            }}
          >
            <Link to="/">Problems</Link>
          </NavigationMenuItem>
          {/* <NavigationMenuItem>
            <Link to="/contests">Contests</Link>
          </NavigationMenuItem> */}
        </NavigationMenuList>
      </NavigationMenu>

      {/* Right Side */}
      <NavigationMenu>
        <NavigationMenuList className="flex space-x-3">
          <NavigationMenuItem>
            <ModeToggle />
          </NavigationMenuItem>
          <NavigationMenuItem>
            <DropdownMenu>
              <DropdownMenuTrigger>
                <Avatar>
                  {avatarUrl ? (
                    <>
                      <AvatarImage src={avatarUrl} />
                      <AvatarFallback>
                        {username?.charAt(0) ?? '?'}
                      </AvatarFallback>
                    </>
                  ) : (
                    <AvatarFallback>
                      {username?.charAt(0) ?? '?'}
                    </AvatarFallback>
                  )}
                </Avatar>
              </DropdownMenuTrigger>
              <DropdownMenuContent>
                <DropdownMenuLabel>{username}</DropdownMenuLabel>
                <DropdownMenuSeparator />
                <Link to={`/users/${username}`}>
                  <DropdownMenuItem className="cursor-pointer">
                    Profile
                  </DropdownMenuItem>
                </Link>
                <DropdownMenuItem
                  onClick={() => {
                    localStorage.clear()
                    navigate('/login')
                  }}
                  className="cursor-pointer"
                >
                  Logout
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </NavigationMenuItem>
        </NavigationMenuList>
      </NavigationMenu>
    </div>
  )
}
