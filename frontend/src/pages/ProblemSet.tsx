import axios from "axios";
import { useState, useEffect } from "react";

export function ProblemSet() {
  const [usermame, setUsername] = useState<string>("");

  interface UserInfo {
    username: string
    password: string
  }

  useEffect(() => {
    const getUserInfo = async () => {
      const token = localStorage.getItem("token")
      const userInfo = await axios.get<UserInfo>("http://localhost/api/users/me", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }); 
      setUsername(userInfo.data.username)
    }

    getUserInfo()
  }, [])

  return (
    <div>
        Username = "{ usermame }"
    </div>
  );
}
