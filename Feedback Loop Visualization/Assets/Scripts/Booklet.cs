using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class Booklet : MonoBehaviour
{
    [SerializeField] GameObject[] bricks;
    [SerializeField] Camera camera;
    [SerializeField] TextMeshProUGUI stepText;

    int currentBrick = 0;
    int nextBrick = 0;
    int previousBrick = 0;

    CameraMovement cameraMovement;

    // Start is called before the first frame update
    void Start()
    {
        cameraMovement = camera.GetComponent<CameraMovement>();
        stepText.text = "Step " + (currentBrick + 1) + " of " + bricks.Length;
    }

    public void NextStep()
    {
        if (currentBrick < bricks.Length - 1)
        {
            nextBrick = currentBrick + 1;
            bricks[nextBrick].SetActive(true);
            currentBrick++;
            stepText.text = "Step " + (currentBrick + 1) + " of " + bricks.Length;
            cameraMovement.target = bricks[currentBrick].transform;
        }
    }

    public void PreviousStep()
    {
        if (currentBrick > 0)
        {
            previousBrick = currentBrick - 1;
            bricks[currentBrick].SetActive(false);
            bricks[previousBrick].SetActive(true);
            currentBrick--;
            stepText.text = "Step " + (currentBrick + 1) + " of " + bricks.Length;
            cameraMovement.target = bricks[currentBrick].transform;
        }
    }
}
