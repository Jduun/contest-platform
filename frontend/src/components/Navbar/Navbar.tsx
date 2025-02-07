import { Link } from 'react-router-dom'
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuList,
} from '@/components/ui/navigation-menu'
import { ModeToggle } from '@/components/ui/mode-toggle'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { useAtom } from 'jotai'
import { usernameAtom } from '@/store/atoms'

export function Navbar() {
  const [username, _setUsername] = useAtom(usernameAtom)

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
                <AvatarImage src="https://github.com/shadcn.png" />
                <AvatarFallback>{username.charAt(0)}</AvatarFallback>
              </Avatar>
            </Link>
          </NavigationMenuItem>
        </NavigationMenuList>
      </NavigationMenu>
    </div>
  )
}
