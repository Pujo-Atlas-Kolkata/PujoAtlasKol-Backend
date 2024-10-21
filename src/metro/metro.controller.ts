import { Controller, Get, Param, Post, Body, Delete } from '@nestjs/common';
import { MetroService } from './metro.service';
import { MetroDto } from './metro.entity';
import { ApiResponse } from './metro.response';
import { Status } from './enum/status.enum';

@Controller('metro')
export class MetroController {
  constructor(private readonly metroService: MetroService) {}

  @Get('/list')
  async findAll(): Promise<ApiResponse<MetroDto[]>> {
    const metros = await this.metroService.findAll();
    const result = metros.map((metro) => {
      return {
        ...metro,
      };
    });
  
    return new ApiResponse(result, Status.SUCCESS);
  }

  @Get(':id')
  async findOne(
    @Param('id') id: string
  ): Promise<ApiResponse<MetroDto | string>> {
    const metro = await this.metroService.findOne(id);
    if (!metro) {
      return new ApiResponse(`Metro with ID ${id} not found`, Status.FAILED);
    }
    return new ApiResponse(metro, Status.SUCCESS);
  }

  @Post('/add')
  async create(
    @Body() metroDto: Omit<MetroDto, 'id' | 'created_at' | 'updated_at'>
  ): Promise<ApiResponse<MetroDto>> {
    const createdMetro = await this.metroService.create(metroDto);
    return new ApiResponse(createdMetro, Status.SUCCESS);
  }

  @Delete(':id')
  async delete(
    @Param('id') id: string
  ): Promise<ApiResponse<MetroDto | string>> {
    const deletedMetro = await this.metroService.deleteMetro(id);
    if (deletedMetro === undefined) {
      return new ApiResponse(`Metro with ID ${id} not found`, Status.FAILED);
    }

  }
}
