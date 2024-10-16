import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { MetroModule } from './metro/metro.module';
import { DatabaseModule } from 'db/database.module';

@Module({
  imports: [DatabaseModule, MetroModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
