import { Controller, Get, Param } from '@nestjs/common';
import { MetroService } from './metro.service';
import { Metro } from './metro.entity';

@Controller('metro')
export class MetroController {
  constructor(private readonly metroService: MetroService) {}

  @Get()
  findAll(): Metro[] {
    return this.metroService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string): Metro | undefined {
    return this.metroService.findOne(+id);
  }
}
