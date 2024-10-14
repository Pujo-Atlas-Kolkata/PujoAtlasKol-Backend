import { Injectable } from '@nestjs/common';
import { Metro } from './metro.entity';

@Injectable()
export class MetroService {
  private metros: Metro[] = [
    {
      id: 1,
      lat: 40.7128,
      lon: -74.006,
      name: 'Kavi Subhash',
      station_code: 'KKSO',
      platform_type: 'side platform',
      line: ['BLUE', 'ORANGE'],
      created_at: new Date(),
      updated_at: new Date(),
    },
  ];

  findAll(): Metro[] {
    return this.metros;
  }

  findOne(id: number): Metro | undefined {
    return this.metros.find((metro) => metro.id === id);
  }
}
