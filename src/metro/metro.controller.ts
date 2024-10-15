import { Controller, Get, NotFoundException, Param } from '@nestjs/common';
import { MetroService } from './metro.service';
import { MetroDto } from './metro.entity';
import { ApiResponse } from './metro.response';
import { Status } from './enum/status.enum';

@Controller('metro')
export class MetroController {
  constructor(private readonly metroService: MetroService) {}

  @Get()
  findAll(): ApiResponse<MetroDto[]> {
    const metros = this.metroService.findAll();
    return new ApiResponse(metros, Status.SUCCESS);
  }

  @Get(':id')
  findOne(@Param('id') id: string): ApiResponse<MetroDto> {
    const metro = this.metroService.findOne(+id);
    if (!metro) {
      throw new NotFoundException(`Metro with ID ${id} not found`);
    }
    return new ApiResponse(metro, Status.SUCCESS);
  }
}
