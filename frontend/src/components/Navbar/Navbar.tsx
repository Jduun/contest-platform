import axios, { AxiosError } from 'axios'
import React, { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuIndicator,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
  NavigationMenuViewport,
  navigationMenuTriggerStyle,
} from '@/components/ui/navigation-menu'
import { ModeToggle } from '@/components/ui/mode-toggle'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { useAtom } from 'jotai'
import { usernameAtom } from '@/store/atoms'

import { CalendarIcon } from 'lucide-react'
import { Button } from '@/components/ui/button'
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from '@/components/ui/hover-card'

export function Navbar() {
  const [username, setUsername] = useAtom(usernameAtom)

  return (
    <div className="flex justify-between items-center my-2">
      {/* Left Side */}
      <NavigationMenu>
        <NavigationMenuList className="flex space-x-6">
          <NavigationMenuItem>
            <Link to="/">Задачи</Link>
          </NavigationMenuItem>
          <NavigationMenuItem>
            <Link to="/contests">Контесты</Link>
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
            <Avatar>
              <AvatarImage src="https://github.com/shadcn.png" />
              <AvatarFallback>
                {username.charAt(0).toUpperCase()}
              </AvatarFallback>
            </Avatar>
          </NavigationMenuItem>
        </NavigationMenuList>
      </NavigationMenu>
    </div>
  )
}
