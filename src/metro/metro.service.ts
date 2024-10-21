import { Injectable, Inject } from '@nestjs/common';
import { Repository } from 'typeorm';
import { Metro } from './metro.entity';
import { MetroDto } from './metro.entity';

@Injectable()
export class MetroService {
  constructor(
    @Inject('METRO_REPOSITORY')
    private metroRepository: Repository<Metro>
  ) {}

  async findAll(): Promise<MetroDto[]> {
    const metros = await this.metroRepository.find();
    return metros.map((metro) => this.toDto(metro));
  }

  async findOne(id: string): Promise<MetroDto | undefined> {
    const metro = await this.metroRepository.findOne({ where: { id } });
    return metro ? this.toDto(metro) : undefined;
  }

  async create(
    metroDto: Omit<MetroDto, 'id' | 'created_at' | 'updated_at'>
  ): Promise<MetroDto> {
    const metro = this.metroRepository.create({
      ...metroDto,
      created_at: new Date(),
      updated_at: new Date(),
    });
    await this.metroRepository.save(metro);
    return this.toDto(metro);
  }

  async deleteMetro(id: string): Promise<void |undefined> {
    const result = await this.metroRepository.delete(id);
    if (result.affected === 0) {
    return undefined
    }
    return 
  }

  private toDto(metro: Metro): MetroDto {
    return {
      id: metro.id,
      lat: metro.lat,
      lon: metro.lon,
      name: metro.name,
      station_code: metro.station_code,
      line: metro.line,
      created_at: metro.created_at.getTime(),
      updated_at: metro.updated_at.getTime(),
    };
  }
}
