import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { MetroModule } from './metro/metro.module';
import { DatabaseModule } from 'db/database.module';
import { PujoModule } from './pujo/pujo.module';
import { EventModule } from './event/event.module';

@Module({
  imports: [DatabaseModule, MetroModule, PujoModule, EventModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
