using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class ImageChanger : MonoBehaviour
{
    public Image[] images;
    public Sprite[] imageSprites;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    public void ChangeImage(int imageIndex, int spriteIndex)
    {
        images[imageIndex].sprite = imageSprites[spriteIndex];
    }
}
