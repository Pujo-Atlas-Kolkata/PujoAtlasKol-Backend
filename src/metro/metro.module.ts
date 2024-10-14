import { Module } from '@nestjs/common';
import { MetroController } from './metro.controller';
import { MetroService } from './metro.service';

@Module({
  controllers: [MetroController],
  providers: [MetroService],
})
export class MetroModule {}
