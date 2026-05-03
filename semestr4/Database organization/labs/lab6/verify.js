const { PrismaClient, Prisma, MessageRole } = require('@prisma/client');

const prisma = new PrismaClient();

async function main() {
  const country = await prisma.country.upsert({
    where: { countryName: 'Ukraine' },
    update: {},
    create: { countryName: 'Ukraine' },
  });

  const user = await prisma.user.upsert({
    where: { userName: 'prisma_tester' },
    update: { isActive: true },
    create: {
      firstName: 'Prisma',
      secondName: 'Tester',
      userName: 'prisma_tester',
      email: 'prisma.tester@example.com',
      countryId: country.countryId,
      createdAt: new Date('2026-04-23'),
      isActive: true,
    },
  });

  const family = await prisma.aiModelFamily.upsert({
    where: { familyName: 'GPT' },
    update: {},
    create: { familyName: 'GPT' },
  });

  const model = await prisma.aiModel.upsert({
    where: {
      familyId_modelVersion: {
        familyId: family.familyId,
        modelVersion: '4.1',
      },
    },
    update: {},
    create: {
      familyId: family.familyId,
      modelVersion: '4.1',
    },
  });

  let chat = await prisma.chat.findFirst({
    where: {
      ownerUserId: user.userId,
      title: 'Prisma migration check',
    },
  });

  if (!chat) {
    chat = await prisma.chat.create({
      data: {
        ownerUserId: user.userId,
        title: 'Prisma migration check',
        createdAt: new Date('2026-04-23'),
      },
    });
  }

  const userMessage = await prisma.message.create({
    data: {
      chatId: chat.chatId,
      roleM: MessageRole.user,
      contentM: 'Check Prisma migrations.',
      createdAt: new Date('2026-04-23T13:00:00'),
    },
  });

  const aiMessage = await prisma.message.create({
    data: {
      chatId: chat.chatId,
      roleM: MessageRole.ai_model,
      contentM: 'Migrations were applied successfully.',
      createdAt: new Date('2026-04-23T13:00:05'),
    },
  });

  await prisma.attachment.create({
    data: {
      messageId: userMessage.messageId,
      fileName: 'migration-check.txt',
      sizeBytes: BigInt(2048),
      uploadedAt: new Date('2026-04-23T13:00:01'),
    },
  });

  await prisma.generation.create({
    data: {
      modelId: model.modelId,
      messageId: aiMessage.messageId,
      createdAt: new Date('2026-04-23T13:00:05'),
      parameters: {
        create: [
          { parameterName: 'temperature', parameterValue: new Prisma.Decimal('0.3000') },
          { parameterName: 'max_tokens', parameterValue: new Prisma.Decimal('120') },
          { parameterName: 'top_p', parameterValue: new Prisma.Decimal('0.9000') },
        ],
      },
    },
  });

  const tag = await prisma.chatTag.upsert({
    where: { tagName: 'migration-check' },
    update: {},
    create: { tagName: 'migration-check' },
  });

  await prisma.chatTagAssignment.upsert({
    where: {
      chatId_tagId: {
        chatId: chat.chatId,
        tagId: tag.tagId,
      },
    },
    update: {},
    create: {
      chatId: chat.chatId,
      tagId: tag.tagId,
    },
  });

  const result = await prisma.chat.findMany({
    where: { ownerUserId: user.userId },
    include: {
      owner: true,
      tagAssignments: { include: { tag: true } },
      messages: {
        include: {
          attachments: true,
          generation: {
            include: {
              model: { include: { family: true } },
              parameters: true,
            },
          },
        },
      },
    },
  });

  console.dir(result, { depth: null });
}

main()
  .catch((error) => {
    console.error(error);
    process.exitCode = 1;
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
