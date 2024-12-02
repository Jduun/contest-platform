import { Link } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export function SignUpForm() {
  const navigate = useNavigate();
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [error, setError] = useState<string | null>(null);

  const handleSignUp = async () => {
    setError(null);
    try {
      const registerResponse = await axios.post("http://localhost/api/register", { username, password });
      // Use URLSearchParams to send data in x-www-form-urlencoded format
      const params = new URLSearchParams();
      params.append("username", username);
      params.append("password", password);

      const loginResponse = await axios.post("http://localhost/api/login", params, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });

      const { access_token, token_type } = loginResponse.data;
      // Save the token to localStorage
      localStorage.setItem("token", `${access_token}`);
      alert("Регистрация прошла успешно!");
      navigate("/")
    } catch (err: any) {
      setError(err.response?.data?.detail || "An unexpected error occurred");
    }
  };

  return (
    <Card className="w-[350px]">
      <CardHeader>
        <CardTitle className="text-2xl">Регистрация</CardTitle>
        <CardDescription>Придумайте имя пользователя и пароль</CardDescription>
      </CardHeader>
      <CardContent>
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSignUp();
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
          {error && (
            <p className="text-red-500 text-sm mt-2">
              {error}
            </p>
          )}
        </form>
      </CardContent>
      <CardFooter className="flex flex-col">
        <div className="w-full">
          <Button
            type="submit"
            className="w-full"
            onClick={(e) => {
              e.preventDefault();
              handleSignUp();
            }}
          >
            Создать аккаунт
          </Button>
        </div>
        <div className="mt-4 text-center text-sm">
          У Вас уже есть аккаунт?{" "}
        </div>
        <div className="text-center text-sm">
          <Link to="/login" className="underline">
            Войдите в аккаунт здесь
          </Link>
        </div>

      </CardFooter>
    </Card>
  );
}