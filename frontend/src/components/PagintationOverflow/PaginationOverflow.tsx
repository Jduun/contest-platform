import React from 'react'

import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from '@/components/ui/pagination'

interface PaginationProps {
  basePath: string
  lastPage: number
  currentPage: number
  visibleCount?: number
}

const PaginationOverflow: React.FC<PaginationProps> = ({
  basePath,
  lastPage,
  currentPage,
  visibleCount = 3,
}) => {
  if (!basePath || !lastPage || !currentPage) {
    return <div></div>
  }

  if (visibleCount > lastPage) return <div></div>
  if (currentPage > lastPage || currentPage < 1) return null

  const navigationLinkHref = (pageNumber: number) => {
    return `${basePath}?page=${pageNumber}`
  }

  const renderPageLink = (pageNumber: number) => (
    <PaginationItem key={pageNumber}>
      <PaginationLink
        href={navigationLinkHref(pageNumber)}
        isActive={pageNumber === currentPage}
      >
        {pageNumber}
      </PaginationLink>
    </PaginationItem>
  )

  let numbers = [...Array(visibleCount)]
  if (currentPage <= Math.ceil(visibleCount / 2)) {
    numbers = numbers.map((_, i) => i + 1)
  } else if (
    currentPage > Math.ceil(visibleCount / 2) &&
    currentPage <= lastPage - Math.ceil(visibleCount / 2)
  ) {
    numbers = numbers.map(
      (_, i) => i + 1 + currentPage - Math.ceil(visibleCount / 2),
    )
  } else if (currentPage > lastPage - Math.ceil(visibleCount / 2)) {
    numbers = numbers.map((_, i) => i + lastPage - visibleCount + 1)
  }

  return (
    <Pagination>
      <PaginationContent>
        <PaginationItem>
          <PaginationPrevious
            href={navigationLinkHref(currentPage - 1)}
            aria-disabled={currentPage <= 1}
            tabIndex={currentPage <= 1 ? -1 : undefined}
            className={
              currentPage <= 1 ? 'pointer-events-none opacity-50' : undefined
            }
          />
        </PaginationItem>

        {numbers.at(0) !== 1 && (
          <PaginationItem>
            <PaginationEllipsis />
          </PaginationItem>
        )}

        {numbers.map((n) => renderPageLink(n))}

        {numbers.at(-1) !== lastPage && (
          <PaginationItem>
            <PaginationEllipsis />
          </PaginationItem>
        )}

        <PaginationItem>
          <PaginationNext
            href={navigationLinkHref(currentPage + 1)}
            aria-disabled={currentPage === lastPage}
            tabIndex={currentPage === lastPage ? -1 : undefined}
            className={
              currentPage === lastPage
                ? 'pointer-events-none opacity-50'
                : undefined
            }
          />
        </PaginationItem>
      </PaginationContent>
    </Pagination>
  )
}

export default PaginationOverflow
