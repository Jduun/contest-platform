import axios, { AxiosError } from "axios";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Navbar } from "@/components/Navbar/Navbar";
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog"
import { useAtom } from 'jotai'
import { usernameAtom } from '@/store/atoms'
import { ContestCard } from "@/components/ContestCard/ContestCard";
import { Button } from "@/components/ui/button"
import moment from "moment";

interface UserInfo {
  username: string
}

interface Contest {
  id: string
  name: string
  start_time: string
  end_time: string
}

export function ContestList() {
  const navigate = useNavigate()
  const [username, setUsername] = useAtom(usernameAtom)
  const [contests, setContests] = useState<Contest[] | []>([])

  useEffect(() => {
    const getUserInfo = async () => {
      const token = localStorage.getItem("token")
      await axios.get<UserInfo>("http://localhost/api/users/me", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((response) => {
        setUsername(response.data.username)
      })
      .catch((err: AxiosError) => {
        navigate("/login")
        return
      })
    }
    getUserInfo()

    const getContests = async () => {
      const token = localStorage.getItem("token")
      await axios.get<Contest[]>("http://localhost/api/contests", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        params: {
          offset: 0,
          limit: 10,
        }
      })
      .then((response) => {
        console.log(response.data)
        setContests(response.data)
      })
    }
    getContests()
  }, [])

  return (
    <div className="flex flex-col w-full max-w-[900px] mx-auto">
      <Navbar />
      <div>
        {
          contests.map((contest) => (
              <ContestCard
                key={contest.id}
                id={contest.id}
                name={contest.name}
                start_time={moment(contest.start_time).format("LLL")}
                end_time={moment(contest.end_time).format("LLL")}
              />
          ))
        }
      </div>
      <Pagination>
        <PaginationContent>
          <PaginationItem>
            <PaginationPrevious href="#" />
          </PaginationItem>
          <PaginationItem>
            <PaginationLink href="#">1</PaginationLink>
          </PaginationItem>
          <PaginationItem>
            <PaginationLink href="#">2</PaginationLink>
          </PaginationItem>
          <PaginationItem>
            <PaginationEllipsis />
          </PaginationItem>
          <PaginationItem>
            <PaginationNext href="#" />
          </PaginationItem>
        </PaginationContent>
      </Pagination>
    </div>
  );
}
