import { Injectable } from '@nestjs/common';
import { Metro } from './metro.entity';
import { MetroDto } from './metro.entity';

@Injectable()
export class MetroService {
  private metros: Metro[] = [
    {
      id: 1,
      lat: 40.7128,
      lon: -74.006,
      name: 'Kavi Subhash',
      station_code: 'KKSO',
      line: ['BLUE', 'ORANGE'],
      created_at: Date.now(),
      updated_at: Date.now(),
    },
  ];

  findAll(): MetroDto[] {
    return this.metros.map((metro) => this.toDto(metro));
  }

  findOne(id: number): MetroDto | undefined {
    const metro = this.metros.find((metro) => metro.id === id);
    return metro ? this.toDto(metro) : undefined;
  }

  private toDto(metro: Metro): MetroDto {
    return {
      id: metro.id,
      lat: metro.lat,
      lon: metro.lon,
      name: metro.name,
      station_code: metro.station_code,
      line: metro.line,
      created_at: metro.created_at,
      updated_at: metro.updated_at,
    };
  }
}
