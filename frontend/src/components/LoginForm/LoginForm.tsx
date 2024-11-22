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

export function LoginForm() {
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [error, setError] = useState<string | null>(null);

  const handleLogin = async () => {
    setError(null);
    try {
      // Use URLSearchParams to send data in x-www-form-urlencoded format
      const params = new URLSearchParams();
      params.append("username", username);
      params.append("password", password);

      const response = await axios.post("http://localhost/api/login", params, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });

      const { access_token, token_type } = response.data;
      // Save the token to localStorage
      localStorage.setItem("token", `${token_type} ${access_token}`);
      alert("Login successful!");
    } catch (err: any) {
      setError(err.response?.data?.detail || "An unexpected error occurred");
    }
  };

  return (
    <Card className="w-[350px]">
      <CardHeader>
        <CardTitle className="text-2xl">Войти</CardTitle>
        <CardDescription>Enter your credentials to login to your account.</CardDescription>
      </CardHeader>
      <CardContent>
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleLogin();
          }}
        >
          <div className="grid w-full text-left gap-4">
            <div className="flex flex-col space-y-1.5">
              <Label htmlFor="username">Username</Label>
              <Input
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>
            <div className="flex flex-col space-y-1.5">
              <Label htmlFor="password">Password</Label>
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
              handleLogin();
            }}
          >
            Login
          </Button>
        </div>
        <div className="mt-4 text-center text-sm">
          Don&apos;t have an account?{" "}
          <a href="#" className="underline">
            Sign up
          </a>
        </div>
      </CardFooter>
    </Card>
  );
}
