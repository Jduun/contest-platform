import { VictoryPie } from 'victory'
import { SolvedProblemsStats } from '@/dto'

const difficultyColors: Record<string, string> = {
  easy: '#10B981',
  medium: '#F59E0B',
  hard: '#EF4444',
}

export function ProblemPieChart(stats: SolvedProblemsStats) {
  return (
    <div className="flex py-2">
      <div>
        <VictoryPie
          innerRadius={60}
          radius={35}
          height={120}
          width={120}
          labels={[]}
          data={[
            { x: 'easy', y: stats.easy, fill: difficultyColors['easy'] },
            { x: 'medium', y: stats.medium, fill: difficultyColors['medium'] },
            { x: 'hard', y: stats.hard, fill: difficultyColors['hard'] },
          ]}
          style={{
            data: {
              fill: ({ datum }) => datum.fill,
            },
          }}
        />
      </div>
      <div className="px-4">
        <p className="text-green-500 text-lg">• Easy: {stats.easy}</p>
        <p className="text-yellow-500 text-lg">• Medium: {stats.medium}</p>
        <p className="text-red-500 text-lg">• Hard: {stats.hard}</p>
      </div>
    </div>
  )
}
