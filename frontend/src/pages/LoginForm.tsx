import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import axios from 'axios'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { API_URL } from '@/api'

export function LoginForm() {
  const navigate = useNavigate()
  const [username, setUsername] = useState<string>('')
  const [password, setPassword] = useState<string>('')
  const [error, setError] = useState<string | null>(null)

  const handleLogin = async () => {
    setError(null)
    try {
      // Use URLSearchParams to send data in x-www-form-urlencoded format
      const params = new URLSearchParams()
      params.append('username', username)
      
      params.append('password', password)

      const response = await axios.post(`${API_URL}/api/login`, params, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      })

      const { access_token, token_type: _ } = response.data
      localStorage.setItem('token', `${access_token}`)
      navigate('/')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'An unexpected error occurred')
    }
  }

  return (
    <div className="flex justify-center items-center h-screen">
      <Card className="w-[350px] text-center">
        <CardHeader>
          <CardTitle className="text-2xl">Вход</CardTitle>
          <CardDescription>Введите данные своей учетной записи</CardDescription>
        </CardHeader>
        <CardContent>
          <form
            onSubmit={(e) => {
              e.preventDefault()
              handleLogin()
            }}
          >
            <div className="grid w-full text-left gap-4">
              <div className="flex flex-col space-y-1.5">
                <Label htmlFor="username">Имя пользователя</Label>
                <Input
                  id="username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                />
              </div>
              <div className="flex flex-col space-y-1.5">
                <Label htmlFor="password">Пароль</Label>
                <Input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
            </div>
            {error && <p className="text-red-500 text-sm mt-2">{error}</p>}
          </form>
        </CardContent>
        <CardFooter className="flex flex-col">
          <div className="w-full">
            <Button
              type="submit"
              className="w-full"
              onClick={(e) => {
                e.preventDefault()
                handleLogin()
              }}
            >
              Войти
            </Button>
          </div>
          <div className="mt-4 text-center text-sm">
            У Вас еще нет аккаунта?{' '}
          </div>
          <div className="text-center text-sm">
            <Link to="/signup" className="underline">
              Создайте аккаунт здесь
            </Link>
          </div>
        </CardFooter>
      </Card>
    </div>
  )
}
