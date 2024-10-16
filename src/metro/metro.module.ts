import { Module } from '@nestjs/common';
import { MetroController } from './metro.controller';
import { MetroService } from './metro.service';
import { DatabaseModule } from 'db/database.module';
import { metroProviders } from './metro.provider';

@Module({
  imports: [DatabaseModule],
  controllers: [MetroController],
  providers: [...metroProviders, MetroService],
})
export class MetroModule {}
