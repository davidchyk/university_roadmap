-- DropForeignKey
ALTER TABLE "ai_models" DROP CONSTRAINT "ai_models_family_id_fkey";

-- DropForeignKey
ALTER TABLE "attachments" DROP CONSTRAINT "attachments_message_id_fkey";

-- DropForeignKey
ALTER TABLE "chat_tag_assignments" DROP CONSTRAINT "chat_tag_assignments_chat_id_fkey";

-- DropForeignKey
ALTER TABLE "chat_tag_assignments" DROP CONSTRAINT "chat_tag_assignments_tag_id_fkey";

-- DropForeignKey
ALTER TABLE "chats" DROP CONSTRAINT "chats_owner_user_id_fkey";

-- DropForeignKey
ALTER TABLE "generation_parameters" DROP CONSTRAINT "generation_parameters_generation_id_fkey";

-- DropForeignKey
ALTER TABLE "generations" DROP CONSTRAINT "generations_message_id_fkey";

-- DropForeignKey
ALTER TABLE "generations" DROP CONSTRAINT "generations_model_id_fkey";

-- DropForeignKey
ALTER TABLE "messages" DROP CONSTRAINT "messages_chat_id_fkey";

-- DropForeignKey
ALTER TABLE "users" DROP CONSTRAINT "users_country_id_fkey";

-- AddForeignKey
ALTER TABLE "users" ADD CONSTRAINT "users_country_id_fkey" FOREIGN KEY ("country_id") REFERENCES "countries"("country_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "ai_models" ADD CONSTRAINT "ai_models_family_id_fkey" FOREIGN KEY ("family_id") REFERENCES "ai_model_families"("family_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "chats" ADD CONSTRAINT "chats_owner_user_id_fkey" FOREIGN KEY ("owner_user_id") REFERENCES "users"("user_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "messages" ADD CONSTRAINT "messages_chat_id_fkey" FOREIGN KEY ("chat_id") REFERENCES "chats"("chat_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "attachments" ADD CONSTRAINT "attachments_message_id_fkey" FOREIGN KEY ("message_id") REFERENCES "messages"("message_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "generations" ADD CONSTRAINT "generations_model_id_fkey" FOREIGN KEY ("model_id") REFERENCES "ai_models"("model_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "generations" ADD CONSTRAINT "generations_message_id_fkey" FOREIGN KEY ("message_id") REFERENCES "messages"("message_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "generation_parameters" ADD CONSTRAINT "generation_parameters_generation_id_fkey" FOREIGN KEY ("generation_id") REFERENCES "generations"("generation_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "chat_tag_assignments" ADD CONSTRAINT "chat_tag_assignments_chat_id_fkey" FOREIGN KEY ("chat_id") REFERENCES "chats"("chat_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "chat_tag_assignments" ADD CONSTRAINT "chat_tag_assignments_tag_id_fkey" FOREIGN KEY ("tag_id") REFERENCES "chat_tags"("tag_id") ON DELETE CASCADE ON UPDATE CASCADE;
