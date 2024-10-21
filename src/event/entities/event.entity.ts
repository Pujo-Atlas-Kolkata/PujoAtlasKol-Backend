import { Metro } from 'src/metro/metro.entity';
import { Entity, Column, PrimaryGeneratedColumn, ManyToOne, OneToMany, JoinColumn } from 'typeorm';
import { v4 as uuidv4 } from 'uuid';

@Entity()
export class Event {
  @PrimaryGeneratedColumn('uuid')
  id: string = uuidv4();

  @Column({ length: 100 })
  name: string;

  @Column('float', { nullable: true })
  lat: number;

  @Column('float', { nullable: true })
  lon: number;

  @Column('text')
  address: string;

  @Column('text')
  city: string;

  @Column({ length: 100 })
  zone: string;

  @Column('float', { default: 100.0 })
  search_score: number;

  @Column({ type: 'timestamp', default: () => 'CURRENT_TIMESTAMP', update: false })
  created_at: Date;

  @Column({ type: 'timestamp', nullable: true })
  updated_at: Date;

  @Column('float', { nullable: true, default: null })
  nearest_metro_distance: number;

  @ManyToOne(() => Metro, (metro) => metro.id, { nullable: true, onDelete: 'CASCADE' })
  @JoinColumn({ name: 'metro_id' })
  metro: Metro;

  @OneToMany(() => LastScore, (lastScore) => lastScore.event)
  last_scores: LastScore[];

  toString(): string {
    return this.name;
  }
}

@Entity()
export class LastScore {
  @PrimaryGeneratedColumn('uuid')
  id: string = uuidv4();

  @ManyToOne(() => Event, (event) => event.last_scores, { onDelete: 'CASCADE' })
  @JoinColumn({ name: 'event_id' })
  event: Event;

  @Column()
  name: string;

  @Column('float')
  value: number;

  @Column({ type: 'timestamp', default: () => 'CURRENT_TIMESTAMP', onUpdate: 'CURRENT_TIMESTAMP' })
  last_updated_at: Date;

  toString(): string {
    return `Score: ${this.value} at ${this.last_updated_at}`;
  }
}
