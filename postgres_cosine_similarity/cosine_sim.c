#include "postgres.h"
#include "fmgr.h"
#include <utils/array.h>
#include <catalog/pg_type.h>
#include <math.h>


PG_MODULE_MAGIC;

PG_FUNCTION_INFO_V1(cosine_sim);

Datum
cosine_sim(PG_FUNCTION_ARGS)
{
    float4 vector_norm1, vector_norm2, dot_product, similarity;

    int i, arrayLength1, arrayLength2;
    bool *arrayNullFlags1, *arrayNullFlags2;
    ArrayType *array1, *array2;
    Datum *arrayContent1, *arrayContent2;

    array1 = PG_GETARG_ARRAYTYPE_P(0);
    array2 = PG_GETARG_ARRAYTYPE_P(1);

    // Fill arrayContent arrays
    deconstruct_array(array1, FLOAT4OID, sizeof(float4), true, '_', &arrayContent1, &arrayNullFlags1, &arrayLength1);
    deconstruct_array(array2, FLOAT4OID, sizeof(float4), true, '_', &arrayContent2, &arrayNullFlags2, &arrayLength2);
    
    vector_norm1 = 0.0;
    vector_norm2 = 0.0;
    dot_product = 0.0;

    for (i = 0; i < arrayLength1; i++)
    {
        float4 xi = DatumGetFloat4(arrayContent1[i]);
        float4 yi = DatumGetFloat4(arrayContent2[i]);

        vector_norm1 += xi*xi;
        vector_norm2 += yi*yi;

        dot_product += xi*yi;
    }

    similarity = dot_product / sqrt(vector_norm1 * vector_norm2);

    PG_RETURN_FLOAT4(similarity);
    // PG_RETURN_ARRAYTYPE_P(resultArray);
}
