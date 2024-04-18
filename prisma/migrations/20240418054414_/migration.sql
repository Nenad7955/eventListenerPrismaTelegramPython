-- CreateTable
CREATE TABLE "Event" (
    "id" SERIAL NOT NULL,
    "aixProcessed" TEXT NOT NULL,
    "aixDistributed" TEXT NOT NULL,
    "ethProcessed" TEXT NOT NULL,
    "ethDistributed" TEXT NOT NULL,
    "txhash" TEXT NOT NULL,
    "timestamp" INTEGER NOT NULL,

    CONSTRAINT "Event_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "Event_txhash_key" ON "Event"("txhash");
