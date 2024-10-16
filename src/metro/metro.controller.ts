import { Controller, Get, Param, Post, Body } from '@nestjs/common';
import { MetroService } from './metro.service';
import { MetroDto } from './metro.entity';
import { ApiResponse } from './metro.response';
import { Status } from './enum/status.enum';

@Controller('metro')
export class MetroController {
  constructor(private readonly metroService: MetroService) {}

  @Get()
  async findAll(): Promise<ApiResponse<MetroDto[]>> {
    const metros = await this.metroService.findAll();
    return new ApiResponse(metros, Status.SUCCESS);
  }

  @Get(':id')
  async findOne(
    @Param('id') id: string
  ): Promise<ApiResponse<MetroDto | string>> {
    const metro = await this.metroService.findOne(+id);
    if (!metro) {
      return new ApiResponse(`Metro with ID ${id} not found`, Status.FAILED);
    }
    return new ApiResponse(metro, Status.SUCCESS);
  }

  @Post()
  async create(
    @Body() metroDto: Omit<MetroDto, 'id' | 'created_at' | 'updated_at'>
  ): Promise<ApiResponse<MetroDto>> {
    const createdMetro = await this.metroService.create(metroDto);
    return new ApiResponse(createdMetro, Status.SUCCESS);
  }
}
