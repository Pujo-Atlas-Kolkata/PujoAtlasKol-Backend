import { Entity, Column, PrimaryGeneratedColumn } from 'typeorm';

@Entity()
export class Metro {
  @PrimaryGeneratedColumn()
  id: number;

  @Column('float')
  lat: number;

  @Column('float')
  lon: number;

  @Column()
  name: string;

  @Column({ nullable: true })
  station_code?: string;

  @Column('simple-array')
  line: string[];

  @Column('timestamp')
  created_at: Date;

  @Column('timestamp')
  updated_at: Date;
}

export class MetroDto {
  id: number;
  lat: number;
  lon: number;
  name: string;
  station_code?: string;
  line: string[];
  created_at: number;
  updated_at: number;
}
